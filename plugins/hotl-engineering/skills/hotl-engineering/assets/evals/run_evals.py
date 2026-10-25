#!/usr/bin/env python3
"""
run_evals.py — Eval harness for the retrieval QA agent

L1: Deterministic checks (recall@5, MRR, must_not, refusal)
L2: LLM-as-judge (Bedrock Tokyo / no sampling parameters / median of 3 votes)
    Binarize each axis's graded score (1-5) at the pass line (judge.pass_score) and compute a
    pass rate per axis. Axes are never summed: a sum hides which axis dropped and cannot be
    calibrated against human pass/fail judgments
Gate decision: thresholds.json + baseline comparison → exit code

Usage:
    python evals/run_evals.py \
        --dataset evals/golden/golden.sample.jsonl \
        --suite smoke --thresholds evals/thresholds.json \
        --baseline evals/baseline.json --out evals/out

Environment variables:
    TARGET_ENDPOINT  Base URL of the evaluation target (staging)
    TARGET_API_KEY   Its API key
    JUDGE_MODEL      Bedrock model ID or inference profile ID (required; no default)
    AWS_REGION       ap-northeast-1
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from anthropic import AnthropicBedrock

# No default: never depend silently on a model that will be retired; if unset, do not start evaluating (see main)
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "")
RUBRIC_PATH = Path(__file__).parent / "judge_rubric.md"
AXES = ("correctness", "faithfulness", "completeness")

# Since anthropic SDK 1.0.0 (2026-08-20), messages.create no longer accepts sampling
# parameters; sending one raises TypeError and every judge vote fails. Judge variance is
# handled by the median of several votes. If thresholds.json still sets one, it is not
# sent and the run log says it was ignored
SAMPLING_KEYS = ("temperature", "top_p", "top_k")


def ignored_sampling_keys(cfg: dict) -> list[str]:
    return [key for key in SAMPLING_KEYS if key in cfg]


# 2.1.0 replaced the summed-score gate with a per-axis pass-rate gate. Stop on the old keys instead of ignoring them
RATE_THRESHOLD_KEYS = ("must_pass_rate", "recall_at_5_drop_allowed",
                       "judge_axis_pass_rate_floor", "judge_axis_pass_rate_drop_allowed")
THRESHOLD_KEYS = (*RATE_THRESHOLD_KEYS, "must_not_violations")
LEGACY_THRESHOLD_KEYS = ("judge_total_floor", "judge_total_drop_allowed")
# Tolerance so a value exactly on the boundary (e.g. 0.9 vs 1.0 - 0.1) does not fail on floating-point error
EPSILON = 1e-9


def is_fraction(value) -> bool:
    """Whether value is a finite number from 0 to 1. Reject bool, str, None, NaN, and infinity (they silently make comparisons false)"""
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def validate_thresholds(thresholds: dict) -> None:
    if legacy := [key for key in LEGACY_THRESHOLD_KEYS if key in thresholds]:
        raise ValueError(
            f"thresholds use the summed judge score keys {legacy}, which hotl 2.1.0 replaced with "
            "judge_axis_pass_rate_floor / judge_axis_pass_rate_drop_allowed (see ADJUST.md)")
    if missing := [key for key in THRESHOLD_KEYS if key not in thresholds]:
        raise ValueError(f"thresholds are missing {missing}")
    for key in RATE_THRESHOLD_KEYS:
        if not is_fraction(thresholds[key]):
            raise ValueError(f"threshold {key} must be a finite number from 0 to 1, got {thresholds[key]!r}")
    violations = thresholds["must_not_violations"]
    if type(violations) is not int or violations < 0:
        raise ValueError(f"threshold must_not_violations must be a non-negative integer, got {violations!r}")


def judge_pass_score(cfg: dict) -> int:
    score = cfg.get("pass_score", 4)
    if type(score) is not int or not 2 <= score <= 5:
        raise ValueError("judge pass_score must be an integer from 2 to 5")
    return score


def load_baseline(path: str, pass_score: int) -> dict:
    baseline = json.loads(Path(path).read_text())["summary"]
    if not isinstance(baseline, dict) or not baseline:
        raise ValueError("baseline summary is missing or invalid")
    rates = baseline.get("judge_axis_pass_rate")
    if not isinstance(rates, dict) or set(rates) != set(AXES):
        raise ValueError(
            "baseline has no per-axis judge pass rates (it was written before hotl 2.1.0, which "
            "gated on judge_total_mean): regenerate the baseline with this run_evals.py")
    recall = baseline.get("recall_at_5_mean")
    if recall is not None and not is_fraction(recall):
        raise ValueError(f"baseline recall_at_5_mean must be null or a finite number from 0 to 1, got {recall!r}")
    # A baseline with a missing axis (e.g. a failed run where no case reached the judge) drops that axis's regression check
    if bad := {axis: rate for axis, rate in rates.items() if not is_fraction(rate)}:
        raise ValueError(f"baseline judge pass rates must be finite numbers from 0 to 1, got {bad!r}: "
                         "regenerate the baseline from a complete run")
    if baseline.get("judge_pass_score") != pass_score:
        raise ValueError(
            f"baseline was scored with judge pass_score {baseline.get('judge_pass_score')}, "
            f"not {pass_score}: regenerate the baseline")
    return baseline


# ---------------------------------------------------------------------------
# Target system call (if the interface differs, swap out only this part)
# ---------------------------------------------------------------------------
def call_target(query: str, user_context: dict) -> dict:
    """Call the evaluation target API. Returns: {"answer": str, "retrieved_docs": [{"doc_id":..}]}"""
    endpoint = os.environ["TARGET_ENDPOINT"].rstrip("/") + "/query"
    payload = json.dumps(
        {"query": query, "user_id": user_context.get("user_id")}
    ).encode()
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('TARGET_API_KEY', '')}",
        },
        method="POST",
    )
    for attempt in range(3):  # retry for transient failures
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                raise
            print(f"  retry ({e})", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------------------
# L1: Deterministic checks
# ---------------------------------------------------------------------------
@dataclass
class L1Result:
    recall_at_5: float | None
    mrr: float | None
    must_not_violations: list[str] = field(default_factory=list)
    refusal_expected: bool = False
    hard_fail: bool = False
    hard_fail_reason: str = ""


def eval_l1(case: dict, response: dict) -> L1Result:
    retrieved = [d.get("doc_id") for d in response.get("retrieved_docs", [])]
    expected = case.get("expected_doc_ids") or []
    answer = response.get("answer", "")

    # recall@5 / MRR (skip when expected is empty = no-answer/permission cases)
    recall = mrr = None
    if expected:
        top5 = retrieved[:5]
        recall = sum(1 for d in expected if d in top5) / len(expected)
        ranks = [retrieved.index(d) + 1 for d in expected if d in retrieved]
        mrr = (1.0 / min(ranks)) if ranks else 0.0

    # must_not: check both the answer and the retrieved results (a permission leak fails as soon as it appears in retrieval results)
    violations = []
    haystack = answer + "\n" + "\n".join(map(str, retrieved))
    for pattern in case.get("must_not_include") or []:
        if re.search(pattern, haystack):
            violations.append(pattern)

    res = L1Result(recall_at_5=recall, mrr=mrr, must_not_violations=violations)
    if violations:
        res.hard_fail = True
        res.hard_fail_reason = f"must_not violation: {violations}"
    return res


# ---------------------------------------------------------------------------
# L2: LLM-as-judge (median of 3 votes)
# ---------------------------------------------------------------------------
def make_judge_prompt(case: dict, response: dict, rubric: str) -> str:
    docs = json.dumps(response.get("retrieved_docs", []), ensure_ascii=False)[:8000]
    return f"""You are an evaluator for a retrieval-based QA system. Score strictly according to the rubric below.

<rubric>
{rubric}
</rubric>

<case category="{case['category']}">
<query>{case['query']}</query>
<must_include_facts>{json.dumps(case.get('must_include_facts') or [], ensure_ascii=False)}</must_include_facts>
<reference_answer>{case.get('reference_answer') or '(none)'}</reference_answer>
</case>

<retrieved_docs>{docs}</retrieved_docs>

<answer_under_evaluation>
{response.get('answer', '')}
</answer_under_evaluation>

Output only the JSON specified by the rubric."""


def eval_l2(
    client: AnthropicBedrock, case: dict, response: dict, rubric: str, cfg: dict
) -> dict:
    prompt = make_judge_prompt(case, response, rubric)
    votes: list[dict] = []
    vote_count = cfg.get("votes", 3)
    if type(vote_count) is not int or vote_count < 1:
        raise ValueError("judge votes must be a positive integer")
    for _ in range(vote_count):
        try:
            msg = client.messages.create(
                model=JUDGE_MODEL,
                max_tokens=int(cfg.get("max_tokens", 1024)),
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:  # noqa: BLE001 — do not stop the whole suite for a single judge vote failure
            # The type name alone cannot reveal breaking SDK changes (such as removed arguments),
            # so also print the start of the message
            print(f"  judge vote failed ({type(e).__name__}: {str(e)[:200]})", file=sys.stderr)
            continue
        text = "".join(b.text for b in msg.content if b.type == "text")
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            continue
        try:
            vote = json.loads(m.group(0))
            if not isinstance(vote, dict):
                continue
            if not all(isinstance(vote.get(axis), dict)
                       and type(vote[axis].get("score")) is int
                       and 1 <= vote[axis]["score"] <= 5 for axis in AXES):
                continue
            votes.append(vote)
        except json.JSONDecodeError:
            continue

    if len(votes) != vote_count:
        raise ValueError("incomplete or invalid judge votes")

    result = {}
    for axis in AXES:
        scores = [int(v.get(axis, {}).get("score", 0)) for v in votes]
        med = statistics.median(scores)
        reasons = [v.get(axis, {}).get("reason", "") for v in votes]
        result[axis] = {"score": med, "reason": reasons[0], "votes": scores}
    return result


# ---------------------------------------------------------------------------
# Gate decision
# ---------------------------------------------------------------------------
def gate(summary: dict, thresholds: dict, baseline: dict | None) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if summary["n_cases"] == 0:
        failures.append("no cases selected")
    if summary["infrastructure_failed_ids"]:
        failures.append(f"incomplete evaluation: {summary['infrastructure_failed_ids']}")

    if summary["must_pass_rate"] < thresholds["must_pass_rate"]:
        failures.append(
            f"must-pass case failed: {summary['must_pass_failed_ids']}"
        )
    if summary["must_not_violations"] > thresholds["must_not_violations"]:
        failures.append(f"must_not violations: {summary['must_not_violations']}")
    rates = summary["judge_axis_pass_rate"]
    if summary["n_cases"] and all(rate is None for rate in rates.values()):
        failures.append("no case reached the judge")
    for axis in AXES:
        rate = rates[axis]
        if rate is not None and rate < thresholds["judge_axis_pass_rate_floor"] - EPSILON:
            failures.append(
                f"judge {axis} pass rate {rate:.0%} < absolute floor {thresholds['judge_axis_pass_rate_floor']:.0%}"
            )

    if baseline:
        b_recall = baseline.get("recall_at_5_mean")
        if (
            b_recall is not None
            and summary["recall_at_5_mean"] is not None
            and summary["recall_at_5_mean"] < b_recall - thresholds["recall_at_5_drop_allowed"]
        ):
            failures.append(
                f"recall@5 regression: {summary['recall_at_5_mean']:.3f} < baseline {b_recall:.3f} - {thresholds['recall_at_5_drop_allowed']}"
            )
        drop = thresholds["judge_axis_pass_rate_drop_allowed"]
        for axis in AXES:
            rate, b_rate = rates[axis], baseline["judge_axis_pass_rate"][axis]
            if rate is not None and rate < b_rate - drop - EPSILON:
                failures.append(
                    f"judge {axis} regression: pass rate {rate:.0%} < baseline {b_rate:.0%} - {drop:.0%}"
                )
    return (len(failures) == 0), failures


# ---------------------------------------------------------------------------
# Report generation (read by a human at CP4)
# ---------------------------------------------------------------------------
def write_report(out: Path, summary: dict, results: list[dict], ok: bool, failures: list[str], baseline: dict | None) -> None:
    lines = [
        f"## Eval Report — {'✅ PASS' if ok else '❌ FAIL'}",
        "",
        f"- suite: `{summary['suite']}` / cases: {summary['n_cases']} / judge: `{JUDGE_MODEL}`",
        f"- must-pass: {summary['must_pass_rate']:.0%}  |  must_not violations: {summary['must_not_violations']}",
        f"- recall@5 mean: {fmt(summary['recall_at_5_mean'])}"
        + (f"(baseline {fmt(baseline.get('recall_at_5_mean'))})" if baseline else ""),
        f"- judge pass rate per axis (score ≥ {summary['judge_pass_score']}): "
        + " / ".join(
            f"{axis} {pct(summary['judge_axis_pass_rate'][axis])}"
            + (f"(baseline {pct(baseline['judge_axis_pass_rate'][axis])})" if baseline else "")
            for axis in AXES),
        "- judge mean score per axis (diagnostic only; not used by the gate): "
        + " / ".join(f"{axis} {fmt(summary['judge_axis_mean'][axis])}" for axis in AXES),
        "",
    ]
    if failures:
        lines += ["### Reasons for gate failure", *[f"- {f}" for f in failures], ""]

    fails = [r for r in results if r["failed"]]
    if fails:
        lines.append("### Failed cases (diffs a human should review)")
        lines.append("| id | category | reason | judge (c/f/cp) |")
        lines.append("|---|---|---|---|")
        for r in fails:
            j = r.get("judge") or {}
            js = "/".join(str(j.get(a, {}).get("score", "-")) for a in AXES)
            lines.append(
                f"| {r['id']} | {r['category']} | {r['fail_reason'][:80]} | {js} |"
            )
        lines.append("")
    lines.append(
        "> Gate criteria: evals/thresholds.json / Scoring rubric: evals/judge_rubric.md"
    )
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")


def fmt(v):
    return f"{v:.3f}" if isinstance(v, (int, float)) else "n/a"


def pct(v):
    return f"{v:.0%}" if isinstance(v, (int, float)) else "n/a"


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--suite", choices=["smoke", "full"], default="smoke")
    ap.add_argument("--thresholds", required=True)
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--out", default="evals/out")
    ap.add_argument("--expected-revision", help="Require every target response to identify this deployed revision")
    args = ap.parse_args()
    if not JUDGE_MODEL:
        print("JUDGE_MODEL is not set: choose a judge model enabled in your Bedrock account "
              "(see ADJUST.md)", file=sys.stderr)
        return 2

    all_thresholds = json.loads(Path(args.thresholds).read_text())
    thresholds = all_thresholds[args.suite]
    validate_thresholds(thresholds)
    judge_cfg = all_thresholds.get("judge", {})
    pass_score = judge_pass_score(judge_cfg)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if ignored := ignored_sampling_keys(judge_cfg):
        print(f"judge: ignoring sampling parameters {', '.join(ignored)} "
              "(not accepted by anthropic SDK >= 1.0)", file=sys.stderr)
    rubric = RUBRIC_PATH.read_text(encoding="utf-8")

    # If --baseline is given but the file is missing or broken, never silently disable the comparison
    baseline = load_baseline(args.baseline, pass_score) if args.baseline else None

    cases = [
        json.loads(line)
        for line in Path(args.dataset).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    cases = [c for c in cases if args.suite in c.get("suite", ["full"])]
    print(f"suite={args.suite}, cases={len(cases)}")

    client = AnthropicBedrock(
        aws_region=os.environ.get("AWS_REGION", "ap-northeast-1")
    )

    results: list[dict] = []
    for case in cases:
        print(f"[{case['id']}]")
        row: dict = {"id": case["id"], "category": case["category"],
                     "must_pass": case.get("must_pass", False),
                     "failed": False, "fail_reason": ""}
        try:
            response = call_target(case["query"], case.get("user_context") or {})
            if args.expected_revision and response.get("revision") != args.expected_revision:
                raise ValueError("target revision mismatch")
        except Exception as e:  # noqa: BLE001
            row.update(failed=True, infrastructure_error=True,
                       fail_reason=f"target error or revision mismatch: {type(e).__name__}")
            results.append(row)
            continue

        l1 = eval_l1(case, response)
        row.update(recall_at_5=l1.recall_at_5, mrr=l1.mrr,
                   must_not_violations=l1.must_not_violations)
        if l1.hard_fail:
            row.update(failed=True, fail_reason=l1.hard_fail_reason)
            results.append(row)
            continue  # do not spend judge cost on an L1 hard fail

        try:
            judge = eval_l2(client, case, response, rubric, judge_cfg)
        except Exception as e:  # noqa: BLE001 — preserve a report for incomplete runs
            row.update(failed=True, infrastructure_error=True,
                       fail_reason=f"judge error: {type(e).__name__}")
            results.append(row)
            continue
        # Binarize each axis at the pass line. A case with any axis below it fails, so the report shows it
        judge_pass = {a: judge[a]["score"] >= pass_score for a in AXES}
        row.update(judge=judge, judge_pass=judge_pass)
        below = [a for a in AXES if not judge_pass[a]]
        if below:
            kind = "must-pass case" if case.get("must_pass") else "case"
            row.update(failed=True, fail_reason=f"{kind} below judge pass line on {', '.join(below)}")
        results.append(row)

    # --- Aggregation ---
    recalls = [r["recall_at_5"] for r in results if r.get("recall_at_5") is not None]
    judged = [r for r in results if "judge_pass" in r]
    mp = [r for r in results if r["must_pass"]]
    mp_failed = [r["id"] for r in mp if r["failed"]]
    summary = {
        "suite": args.suite,
        "n_cases": len(results),
        "expected_revision": args.expected_revision,
        "infrastructure_failed_ids": [r["id"] for r in results if r.get("infrastructure_error")],
        "recall_at_5_mean": statistics.mean(recalls) if recalls else None,
        "judge_pass_score": pass_score,
        "judge_axis_pass_rate": {
            a: (sum(r["judge_pass"][a] for r in judged) / len(judged)) if judged else None for a in AXES},
        "judge_axis_mean": {
            a: statistics.mean(r["judge"][a]["score"] for r in judged) if judged else None for a in AXES},
        "must_pass_rate": 1.0 - (len(mp_failed) / len(mp)) if mp else 1.0,
        "must_pass_failed_ids": mp_failed,
        "must_not_violations": sum(len(r.get("must_not_violations") or []) for r in results),
    }

    ok, failures = gate(summary, thresholds, baseline)
    (out / "results.json").write_text(
        json.dumps({"summary": summary, "results": results},
                   ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    write_report(out, summary, results, ok, failures, baseline)
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    print("GATE:", "PASS ✅" if ok else f"FAIL ❌ {failures}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
