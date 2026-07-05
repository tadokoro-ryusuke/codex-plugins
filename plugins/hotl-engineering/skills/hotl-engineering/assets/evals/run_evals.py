#!/usr/bin/env python3
"""
run_evals.py — Eval harness for the retrieval QA agent

L1: Deterministic checks (recall@5, MRR, must_not, refusal)
L2: LLM-as-judge (Bedrock Tokyo / temperature 0 / median of 3 votes)
Gate decision: thresholds.json + baseline comparison → exit code

Usage:
    python evals/run_evals.py \
        --dataset evals/golden/golden.sample.jsonl \
        --suite smoke --thresholds evals/thresholds.json \
        --baseline evals/baseline.json --out evals/out

Environment variables:
    TARGET_ENDPOINT  Base URL of the evaluation target (staging)
    TARGET_API_KEY   Its API key
    JUDGE_MODEL      Bedrock inference profile ID (default: Sonnet Tokyo)
    AWS_REGION       ap-northeast-1
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from anthropic import AnthropicBedrock

JUDGE_MODEL = os.environ.get(
    "JUDGE_MODEL", "apac.anthropic.claude-sonnet-4-5-20250929-v1:0"
)
RUBRIC_PATH = Path(__file__).parent / "judge_rubric.md"
AXES = ("correctness", "faithfulness", "completeness")


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
    for _ in range(int(cfg.get("votes", 3))):
        try:
            msg = client.messages.create(
                model=JUDGE_MODEL,
                max_tokens=int(cfg.get("max_tokens", 1024)),
                temperature=float(cfg.get("temperature", 0)),
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:  # noqa: BLE001 — do not stop the whole suite for a single judge vote failure
            print(f"  judge vote failed ({e})", file=sys.stderr)
            continue
        text = "".join(b.text for b in msg.content if b.type == "text")
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            continue
        try:
            votes.append(json.loads(m.group(0)))
        except json.JSONDecodeError:
            continue

    if not votes:
        return {a: {"score": 0, "reason": "judge parse failure"} for a in AXES}

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

    if summary["must_pass_rate"] < thresholds["must_pass_rate"]:
        failures.append(
            f"must-pass case failed: {summary['must_pass_failed_ids']}"
        )
    if summary["must_not_violations"] > thresholds["must_not_violations"]:
        failures.append(f"must_not violations: {summary['must_not_violations']}")
    if summary["judge_total_mean"] < thresholds["judge_total_floor"]:
        failures.append(
            f"judge mean {summary['judge_total_mean']:.2f} < absolute floor {thresholds['judge_total_floor']}"
        )

    if baseline:
        b_recall = baseline.get("recall_at_5_mean")
        b_judge = baseline.get("judge_total_mean")
        if (
            b_recall is not None
            and summary["recall_at_5_mean"] is not None
            and summary["recall_at_5_mean"] < b_recall - thresholds["recall_at_5_drop_allowed"]
        ):
            failures.append(
                f"recall@5 regression: {summary['recall_at_5_mean']:.3f} < baseline {b_recall:.3f} - {thresholds['recall_at_5_drop_allowed']}"
            )
        if b_judge is not None and summary["judge_total_mean"] < b_judge - thresholds["judge_total_drop_allowed"]:
            failures.append(
                f"judge regression: {summary['judge_total_mean']:.2f} < baseline {b_judge:.2f} - {thresholds['judge_total_drop_allowed']}"
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
        f"- judge total mean: {summary['judge_total_mean']:.2f} / 15"
        + (f"(baseline {baseline.get('judge_total_mean', 0):.2f})" if baseline else ""),
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


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--suite", choices=["smoke", "full"], default="smoke")
    ap.add_argument("--thresholds", required=True)
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--out", default="evals/out")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    all_thresholds = json.loads(Path(args.thresholds).read_text())
    thresholds = all_thresholds[args.suite]
    judge_cfg = all_thresholds.get("judge", {})
    rubric = RUBRIC_PATH.read_text(encoding="utf-8")

    baseline = None
    if args.baseline and Path(args.baseline).exists():
        baseline = json.loads(Path(args.baseline).read_text()).get("summary")

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
        print(f"[{case['id']}] {case['query'][:40]}…")
        row: dict = {"id": case["id"], "category": case["category"],
                     "must_pass": case.get("must_pass", False),
                     "failed": False, "fail_reason": ""}
        try:
            response = call_target(case["query"], case.get("user_context") or {})
        except Exception as e:  # noqa: BLE001
            row.update(failed=True, fail_reason=f"target error: {e}")
            results.append(row)
            continue

        l1 = eval_l1(case, response)
        row.update(recall_at_5=l1.recall_at_5, mrr=l1.mrr,
                   must_not_violations=l1.must_not_violations)
        if l1.hard_fail:
            row.update(failed=True, fail_reason=l1.hard_fail_reason)
            results.append(row)
            continue  # do not spend judge cost on an L1 hard fail

        judge = eval_l2(client, case, response, rubric, judge_cfg)
        total = sum(judge[a]["score"] for a in AXES)
        row.update(judge=judge, judge_total=total)

        # Pass/fail per case: must_pass requires all judge axes to score >= 4
        if case.get("must_pass") and any(judge[a]["score"] < 4 for a in AXES):
            row.update(failed=True,
                       fail_reason=f"must-pass case below bar (total={total})")
        elif total < 8:  # surface obvious quality issues as individual fails
            row.update(failed=True, fail_reason=f"low judge total ({total})")
        results.append(row)

    # --- Aggregation ---
    recalls = [r["recall_at_5"] for r in results if r.get("recall_at_5") is not None]
    totals = [r["judge_total"] for r in results if "judge_total" in r]
    mp = [r for r in results if r["must_pass"]]
    mp_failed = [r["id"] for r in mp if r["failed"]]
    summary = {
        "suite": args.suite,
        "n_cases": len(results),
        "recall_at_5_mean": statistics.mean(recalls) if recalls else None,
        "judge_total_mean": statistics.mean(totals) if totals else 0.0,
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
