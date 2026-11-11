"""Offline contract tests for shipped delivery gates; never call a model or target."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


ASSETS = Path(__file__).resolve().parents[2] / "plugins/hotl-engineering/skills/hotl-engineering/assets"
VERDICT_GATE = ASSETS / "scripts/check_review_verdicts.py"


class ReviewGateTests(unittest.TestCase):
    def run_gate(self, light, deep=None, **overrides):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for tier, verdict in (("light", light), ("deep", deep)):
                if verdict is not None:
                    folder = root / ("ai-review-verdict-" + tier)
                    folder.mkdir()
                    (folder / "verdict.json").write_text(verdict)
            env = {**os.environ, "VERDICT_DIR": directory, "ENFORCE": "true",
                   "CLASSIFY_RESULT": "success", "TIER2": "false", "IS_DRAFT": "false",
                   "REVIEW_RESULT": "success", "DEEP_RESULT": "skipped",
                   "LIGHT_DOWNLOAD": "success", "DEEP_DOWNLOAD": "success" if deep is not None else "skipped",
                   "EXPECTED_SHA": "a" * 40, **overrides}
            return subprocess.run([sys.executable, str(VERDICT_GATE)], env=env,
                                  capture_output=True, text=True, timeout=5)

    def verdict(self, **overrides):
        return json.dumps({"critical": 0, "high": 0, "head_sha": "a" * 40, **overrides})

    def test_valid_light_review_passes(self):
        result = self.run_gate(self.verdict())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_malformed_or_wrong_revision_cannot_pass(self):
        for verdict in (None, "not json", "{}", "[]", self.verdict(critical=-1),
                        self.verdict(critical=True), self.verdict(high="0"),
                        self.verdict(head_sha="b" * 40)):
            with self.subTest(verdict=verdict):
                result = self.run_gate(verdict)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_critical_and_required_job_failures_block(self):
        for overrides in ({"CLASSIFY_RESULT": "failure"}, {"REVIEW_RESULT": "cancelled"},
                          {"TIER2": "true"}, {"TIER2": ""}):
            with self.subTest(overrides=overrides):
                self.assertEqual(self.run_gate(self.verdict(), **overrides).returncode, 1)
        self.assertEqual(self.run_gate(self.verdict(critical=1)).returncode, 1)

    def test_deep_review_requires_success_and_its_own_valid_verdict(self):
        result = self.run_gate(self.verdict(), self.verdict(), TIER2="true", DEEP_RESULT="success")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_gate(self.verdict(), TIER2="true", DEEP_RESULT="success")
        self.assertEqual(result.returncode, 1)

    def test_failed_artifact_download_blocks_even_with_a_valid_verdict(self):
        # download-artifact v8 reports a digest mismatch only after extracting. The step is continue-on-error, so even
        # if the file remains, the validator gets the download outcome and treats a failure as incomplete evidence
        for overrides in ({"LIGHT_DOWNLOAD": "failure"}, {"LIGHT_DOWNLOAD": ""}):
            with self.subTest(overrides=overrides):
                self.assertEqual(self.run_gate(self.verdict(), **overrides).returncode, 1)
        result = self.run_gate(self.verdict(), self.verdict(), TIER2="true", DEEP_RESULT="success",
                               DEEP_DOWNLOAD="failure")
        self.assertEqual(result.returncode, 1)

    def test_observation_reports_failure_without_enforcing(self):
        result = self.run_gate(None, ENFORCE="false")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INCOMPLETE", result.stdout)


class EvalGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fake_sdk = types.ModuleType("anthropic")
        fake_sdk.AnthropicBedrock = lambda **kwargs: None
        spec = importlib.util.spec_from_file_location("hotl_evals", ASSETS / "evals/run_evals.py")
        cls.runner = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"anthropic": fake_sdk, "hotl_evals": cls.runner}):
            spec.loader.exec_module(cls.runner)

    THRESHOLDS = {"must_pass_rate": 1, "must_not_violations": 0, "recall_at_5_drop_allowed": 0.05,
                  "judge_axis_pass_rate_floor": 0.5, "judge_axis_pass_rate_drop_allowed": 0.1}

    def run_evals(self, cases, target, judge=None, revision=None, missing_baseline=False,
                  baseline=None, thresholds=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cases.jsonl").write_text("\n".join(json.dumps(c) for c in cases))
            (root / "thresholds.json").write_text(json.dumps({
                "smoke": thresholds or self.THRESHOLDS, "judge": {"votes": 3, "pass_score": 4}}))
            args = ["evals", "--dataset", str(root / "cases.jsonl"), "--thresholds",
                    str(root / "thresholds.json"), "--out", str(root / "out")]
            if revision:
                args += ["--expected-revision", revision]
            if missing_baseline:
                args += ["--baseline", str(root / "missing-baseline.json")]
            if baseline is not None:
                (root / "baseline.json").write_text(json.dumps({"summary": baseline}))
                args += ["--baseline", str(root / "baseline.json")]
            scores = {axis: {"score": 5, "reason": "fixture"} for axis in self.runner.AXES}
            with patch.object(sys, "argv", args), patch.object(self.runner, "call_target", side_effect=target), \
                 patch.object(self.runner, "eval_l2", side_effect=judge, return_value=scores), \
                 patch.object(self.runner, "JUDGE_MODEL", "fixture-judge-model"), \
                 contextlib.redirect_stdout(io.StringIO()):
                result = self.runner.main()
            return result, json.loads((root / "out/results.json").read_text())

    def test_judge_model_is_required(self):
        # No default model ID (never depend silently on a model that will be retired). If unset, do not start evaluating
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = ["evals", "--dataset", str(root / "missing.jsonl"), "--thresholds",
                    str(root / "missing.json"), "--out", str(root / "out")]
            with patch.object(sys, "argv", args), patch.object(self.runner, "JUDGE_MODEL", ""), \
                 patch("sys.stderr", new_callable=io.StringIO) as stderr:
                self.assertEqual(self.runner.main(), 2)
            self.assertIn("JUDGE_MODEL", stderr.getvalue())
            self.assertFalse((root / "out").exists())

    def test_cli_without_judge_model_exits_before_evaluating(self):
        # Run the CLI in a separate process without the environment variable, so the import-time default is covered too
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "anthropic.py").write_text("def AnthropicBedrock(**kwargs):\n    return None\n")
            env = {key: value for key, value in os.environ.items() if key != "JUDGE_MODEL"}
            env["PYTHONPATH"] = str(root)
            result = subprocess.run(
                [sys.executable, str(ASSETS / "evals/run_evals.py"), "--dataset", str(root / "missing.jsonl"),
                 "--thresholds", str(root / "missing.json"), "--out", str(root / "out")],
                env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("JUDGE_MODEL", result.stderr)
            self.assertFalse((root / "out").exists())

    def cases(self):
        return [{"id": "must", "category": "answer", "query": "fixture", "suite": ["smoke"], "must_pass": True},
                {"id": "ordinary", "category": "answer", "query": "fixture", "suite": ["smoke"]}]

    def test_target_error_cannot_disappear_from_a_passing_mean(self):
        code, data = self.run_evals(self.cases(), [{"answer": "ok"}, RuntimeError("fixture error")])
        self.assertEqual(code, 1)
        self.assertEqual(data["summary"]["infrastructure_failed_ids"], ["ordinary"])

    def test_judge_error_blocks_and_is_recorded(self):
        scores = {axis: {"score": 5} for axis in self.runner.AXES}
        code, data = self.run_evals(self.cases(), [{"answer": "ok"}] * 2,
                                   judge=[scores, ValueError("invalid judge")])
        self.assertEqual(code, 1)
        self.assertEqual(data["summary"]["infrastructure_failed_ids"], ["ordinary"])

    def test_empty_suite_fails_with_report(self):
        code, data = self.run_evals([], [])
        self.assertEqual(code, 1)
        self.assertEqual(data["summary"]["n_cases"], 0)

    def test_complete_suite_can_pass(self):
        code, data = self.run_evals(self.cases(), [{"answer": "ok"}] * 2)
        self.assertEqual(code, 0)
        self.assertEqual(data["summary"]["n_cases"], 2)

    def test_explicit_missing_baseline_cannot_silently_disable_comparison(self):
        with self.assertRaises(FileNotFoundError):
            self.run_evals(self.cases(), [{"answer": "ok"}] * 2, missing_baseline=True)

    def test_staging_result_must_match_expected_revision(self):
        for actual, expected_code in (("old", 1), (None, 1), ("candidate", 0)):
            with self.subTest(actual=actual):
                code, _ = self.run_evals(self.cases(), [{"answer": "ok", "revision": actual}] * 2,
                                         revision="candidate")
                self.assertEqual(code, expected_code)

    def scores(self, **axes):
        return {axis: {"score": axes.get(axis, 5), "reason": "fixture"} for axis in self.runner.AXES}

    def ordinary_cases(self, n):
        return [{"id": f"case-{i}", "category": "answer", "query": "fixture", "suite": ["smoke"]}
                for i in range(n)]

    def test_each_axis_is_gated_separately_not_as_a_sum(self):
        # Axes are never summed: even with a 12/15 total, block when one axis is below the pass line on every case
        code, data = self.run_evals(self.ordinary_cases(2), [{"answer": "ok"}] * 2,
                                    judge=[self.scores(completeness=2)] * 2)
        self.assertEqual(code, 1)
        rates = data["summary"]["judge_axis_pass_rate"]
        self.assertEqual(rates, {"correctness": 1.0, "faithfulness": 1.0, "completeness": 0.0})
        self.assertNotIn("judge_total_mean", data["summary"])

    def test_case_below_the_pass_line_on_any_axis_is_listed_with_the_axis(self):
        code, data = self.run_evals(self.ordinary_cases(2), [{"answer": "ok"}] * 2,
                                    judge=[self.scores(), self.scores(faithfulness=3)])
        self.assertEqual(code, 0)  # a 50% pass rate meets the 50% floor
        failed = [r for r in data["results"] if r["failed"]]
        self.assertEqual([r["id"] for r in failed], ["case-1"])
        self.assertIn("faithfulness", failed[0]["fail_reason"])
        self.assertEqual(failed[0]["judge_pass"],
                         {"correctness": True, "faithfulness": False, "completeness": True})

    def test_must_pass_case_requires_every_axis_at_the_pass_line(self):
        cases = [{"id": "must", "category": "answer", "query": "fixture", "suite": ["smoke"], "must_pass": True}]
        code, data = self.run_evals(cases, [{"answer": "ok"}], judge=[self.scores(correctness=3)])
        self.assertEqual(code, 1)
        self.assertEqual(data["summary"]["must_pass_failed_ids"], ["must"])

    def test_axis_pass_rate_regression_against_baseline_blocks(self):
        baseline = {"recall_at_5_mean": None, "judge_pass_score": 4,
                    "judge_axis_pass_rate": {axis: 1.0 for axis in self.runner.AXES}}
        code, _ = self.run_evals(self.ordinary_cases(2), [{"answer": "ok"}] * 2,
                                 judge=[self.scores(), self.scores(correctness=1)], baseline=baseline)
        self.assertEqual(code, 1)
        code, _ = self.run_evals(self.ordinary_cases(2), [{"answer": "ok"}] * 2, baseline=baseline)
        self.assertEqual(code, 0)

    def test_regression_boundary_tolerates_float_rounding(self):
        # 0.8 - 0.1 is 0.7000000000000001 in floating point; a drop of exactly the allowance must not count
        thresholds = {**self.THRESHOLDS, "judge_axis_pass_rate_drop_allowed": 0.1}
        judges = [self.scores(correctness=2) if i < 3 else self.scores() for i in range(10)]
        code, data = self.run_evals(self.ordinary_cases(10), [{"answer": "ok"}] * 10, judge=judges,
                                    baseline=self.baseline(correctness=0.8), thresholds=thresholds)
        self.assertEqual(data["summary"]["judge_axis_pass_rate"]["correctness"], 0.7)
        self.assertEqual(code, 0)

    def test_baseline_from_the_summed_score_gate_is_rejected(self):
        # Never silently skip the comparison with a pre-2.1.0 baseline (judge_total_mean only)
        old = {"recall_at_5_mean": 0.9, "judge_total_mean": 13.0}
        with self.assertRaisesRegex(ValueError, "regenerate"):
            self.run_evals(self.ordinary_cases(1), [{"answer": "ok"}], baseline=old)

    def test_baseline_recall_must_be_a_finite_fraction_or_absent(self):
        # A suite with no recall targets has a None baseline. Any other invalid value silently disables the recall check
        for bad in (float("nan"), float("-inf"), -0.1, 1.5, True, "0.9"):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "recall"):
                self.run_evals(self.ordinary_cases(1), [{"answer": "ok"}],
                               baseline={**self.baseline(), "recall_at_5_mean": bad})
        code, _ = self.run_evals(self.ordinary_cases(1), [{"answer": "ok"}],
                                 baseline={**self.baseline(), "recall_at_5_mean": None})
        self.assertEqual(code, 0)

    def test_baseline_with_a_different_pass_line_is_rejected(self):
        other = {"recall_at_5_mean": None, "judge_pass_score": 3,
                 "judge_axis_pass_rate": {axis: 1.0 for axis in self.runner.AXES}}
        with self.assertRaisesRegex(ValueError, "pass_score"):
            self.run_evals(self.ordinary_cases(1), [{"answer": "ok"}], baseline=other)

    def test_legacy_summed_score_thresholds_are_rejected(self):
        legacy = {"must_pass_rate": 1, "must_not_violations": 0, "recall_at_5_drop_allowed": 0.05,
                  "judge_total_drop_allowed": 1.0, "judge_total_floor": 10.5}
        with self.assertRaisesRegex(ValueError, "judge_total_floor"):
            self.run_evals(self.ordinary_cases(1), [{"answer": "ok"}], thresholds=legacy)

    def baseline(self, **rates):
        return {"recall_at_5_mean": None, "judge_pass_score": 4,
                "judge_axis_pass_rate": {axis: rates.get(axis, 1.0) for axis in self.runner.AXES}}

    def test_baseline_rates_must_be_finite_fractions(self):
        # A null or NaN axis silently skips that axis's regression check. Stop before evaluating
        for bad in (None, float("nan"), float("inf"), -0.1, 1.5, True, "1.0"):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "baseline"):
                self.run_evals(self.ordinary_cases(1), [{"answer": "ok"}],
                               baseline=self.baseline(faithfulness=bad))

    def test_rate_thresholds_must_be_finite_fractions(self):
        # A NaN floor or allowed drop makes every comparison false and opens the gate
        for key in ("judge_axis_pass_rate_floor", "judge_axis_pass_rate_drop_allowed",
                    "recall_at_5_drop_allowed", "must_pass_rate"):
            for bad in (float("nan"), float("inf"), -0.1, 1.1, "0.8", True, None):
                with self.subTest(key=key, bad=bad), self.assertRaisesRegex(ValueError, key):
                    self.runner.validate_thresholds({**self.THRESHOLDS, key: bad})
        for bad in (-1, 0.5, True, "0", float("nan")):
            with self.subTest(must_not_violations=bad), self.assertRaisesRegex(ValueError, "must_not_violations"):
                self.runner.validate_thresholds({**self.THRESHOLDS, "must_not_violations": bad})

    def test_score_at_the_pass_line_passes_and_below_fails(self):
        code, data = self.run_evals(self.ordinary_cases(2), [{"answer": "ok"}] * 2,
                                    judge=[self.scores(correctness=4), self.scores(correctness=3.5)])
        self.assertEqual([r["judge_pass"]["correctness"] for r in data["results"]], [True, False])
        self.assertEqual(data["summary"]["judge_axis_pass_rate"]["correctness"], 0.5)

    def test_pass_line_comes_from_the_judge_config(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cases.jsonl").write_text(json.dumps(self.ordinary_cases(1)[0]))
            (root / "thresholds.json").write_text(json.dumps({
                "smoke": self.THRESHOLDS, "judge": {"votes": 3, "pass_score": 3}}))
            args = ["evals", "--dataset", str(root / "cases.jsonl"), "--thresholds",
                    str(root / "thresholds.json"), "--out", str(root / "out")]
            with patch.object(sys, "argv", args), \
                 patch.object(self.runner, "call_target", side_effect=[{"answer": "ok"}]), \
                 patch.object(self.runner, "eval_l2", side_effect=[self.scores(completeness=3)]), \
                 patch.object(self.runner, "JUDGE_MODEL", "fixture-judge-model"), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.runner.main(), 0)
            data = json.loads((root / "out/results.json").read_text())
        self.assertEqual(data["summary"]["judge_pass_score"], 3)
        self.assertTrue(data["results"][0]["judge_pass"]["completeness"])

    def test_even_vote_medians_are_compared_with_the_pass_line(self):
        # With an even vote count the median can be x.5. 3.5 misses a pass line of 4; 4.5 meets it
        for votes, expected in (([3, 4], False), ([4, 5], True)):
            contents = [types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text=json.dumps({
                axis: {"score": score, "reason": "fixture"} for axis in self.runner.AXES}))]) for score in votes]
            client = types.SimpleNamespace(messages=types.SimpleNamespace(create=Mock(side_effect=contents)))
            judge = self.runner.eval_l2(client, self.cases()[0], {}, "rubric", {"votes": 2})
            with self.subTest(votes=votes):
                self.assertEqual(judge["correctness"]["score"] >= 4, expected)

    def test_regression_uses_the_allowed_drop_on_every_axis(self):
        # Keep the absolute floor (50%) satisfied and move only the drop from a 100% baseline. The allowed drop is 10 points
        thresholds = {**self.THRESHOLDS, "judge_axis_pass_rate_drop_allowed": 0.1}
        for axis in self.runner.AXES:
            for failing, expected in ((0, 0), (1, 0), (2, 1)):  # failures out of 10: a 0%, 10% (boundary), and 20% drop
                judges = [self.scores(**{axis: 2}) if i < failing else self.scores() for i in range(10)]
                with self.subTest(axis=axis, failing=failing):
                    code, _ = self.run_evals(self.ordinary_cases(10), [{"answer": "ok"}] * 10, judge=judges,
                                             baseline=self.baseline(), thresholds=thresholds)
                    self.assertEqual(code, expected)

    def test_shipped_thresholds_are_valid_for_every_suite(self):
        shipped = json.loads((ASSETS / "evals/thresholds.json").read_text())
        for suite in ("smoke", "full"):
            with self.subTest(suite=suite):
                self.runner.validate_thresholds(shipped[suite])
        self.assertEqual(shipped["judge"]["pass_score"], 4)

    def test_invalid_judge_scores_and_incomplete_votes_are_rejected(self):
        for values in ([5], [5, 5, 99], [5, 5, True], [5, 5, 5]):
            contents = [types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text=json.dumps({
                axis: {"score": score, "reason": "fixture"} for axis in self.runner.AXES}))]) for score in values]
            client = types.SimpleNamespace(messages=types.SimpleNamespace(create=Mock(side_effect=contents)))
            with self.subTest(values=values):
                if values == [5, 5, 5]:
                    self.assertEqual(self.runner.eval_l2(client, self.cases()[0], {}, "rubric", {})["correctness"]["score"], 5)
                else:
                    with self.assertRaises(ValueError):
                        self.runner.eval_l2(client, self.cases()[0], {}, "rubric", {})


class JudgeSamplingTests(unittest.TestCase):
    """Never send sampling parameters (temperature / top_p / top_k) to the judge.

    Since anthropic SDK 1.0.0 (2026-08-20), messages.create rejects them and every vote fails
    with TypeError. If thresholds.json still sets one, it is not sent and the run says so.
    """

    MODELS = ("apac.anthropic.claude-sonnet-4-5-20250929-v1:0",
              "anthropic.claude-haiku-4-5-20251001-v1:0",
              "anthropic.claude-opus-4-7",
              "arn:aws:bedrock:ap-northeast-1:000000000000:application-inference-profile/fixture")
    SAMPLING = {"temperature": 0, "top_p": 0.9, "top_k": 5}

    @classmethod
    def setUpClass(cls):
        EvalGateTests.setUpClass()
        cls.runner = EvalGateTests.runner

    def judge_params(self, model, cfg):
        vote = json.dumps({axis: {"score": 5, "reason": "fixture"} for axis in self.runner.AXES})
        message = types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text=vote)])
        create = Mock(return_value=message)
        client = types.SimpleNamespace(messages=types.SimpleNamespace(create=create))
        case = {"id": "fixture", "category": "answer", "query": "fixture"}
        with patch.object(self.runner, "JUDGE_MODEL", model):
            self.runner.eval_l2(client, case, {}, "rubric", cfg)
        self.assertEqual(create.call_count, cfg.get("votes", 3))
        return create.call_args.kwargs

    def test_sampling_parameters_are_never_sent(self):
        for model in self.MODELS:
            with self.subTest(model=model):
                params = self.judge_params(model, dict(self.SAMPLING))
                self.assertFalse(set(self.SAMPLING) & set(params))
                self.assertIn("max_tokens", params)

    def test_configured_sampling_parameters_are_reported_as_ignored(self):
        self.assertEqual(self.runner.ignored_sampling_keys({"votes": 3, **self.SAMPLING}),
                         ["temperature", "top_p", "top_k"])
        self.assertEqual(self.runner.ignored_sampling_keys({"votes": 3}), [])

    def test_judge_failure_reports_the_sdk_error_message(self):
        # The type name alone cannot reveal breaking SDK changes such as removed arguments
        error = TypeError("create() got an unexpected keyword argument 'temperature'")
        client = types.SimpleNamespace(messages=types.SimpleNamespace(create=Mock(side_effect=error)))
        case = {"id": "fixture", "category": "answer", "query": "fixture"}
        with patch("sys.stderr", new_callable=io.StringIO) as stderr, self.assertRaises(ValueError):
            self.runner.eval_l2(client, case, {}, "rubric", {"votes": 1})
        self.assertIn("unexpected keyword argument 'temperature'", stderr.getvalue())


def load_eval_runner():
    """Load run_evals.py with a stub anthropic SDK."""
    EvalGateTests.setUpClass()
    return EvalGateTests.runner


AXES_FOR_TESTS = ("correctness", "faithfulness", "completeness")


class JudgeVoteDiagnosticsTests(unittest.TestCase):
    """When a vote is dropped, print the reason and stop_reason (and stop_details if present) to stderr.

    A judge with thinking on by default counts thinking toward max_tokens and can stop before the JSON
    is complete. Without the reason, only the final "incomplete or invalid judge votes" remains.
    The judge's reply text can contain confidential golden-set data, so it never goes to the log.
    """

    CASE = {"id": "fixture", "category": "answer", "query": "fixture"}

    @classmethod
    def setUpClass(cls):
        cls.runner = load_eval_runner()

    def message(self, text=None, stop_reason="end_turn", stop_details=None, thinking=False):
        content = []
        if thinking:
            content.append(types.SimpleNamespace(type="thinking", thinking=""))
        if text is not None:
            content.append(types.SimpleNamespace(type="text", text=text))
        return types.SimpleNamespace(content=content, stop_reason=stop_reason, stop_details=stop_details)

    def dropped(self, message):
        create = Mock(return_value=message)
        client = types.SimpleNamespace(messages=types.SimpleNamespace(create=create))
        with patch("sys.stderr", new_callable=io.StringIO) as stderr, self.assertRaises(ValueError):
            self.runner.eval_l2(client, self.CASE, {}, "rubric", {"votes": 1})
        return stderr.getvalue()

    def test_each_silent_drop_path_reports_its_reason_and_stop_reason(self):
        complete = {axis: {"score": 5, "reason": "fixture"} for axis in AXES_FOR_TESTS}
        cases = {
            "no JSON": "SECRET_FIXTURE and no JSON",
            # Cut at max_tokens, the regular expression hits an unclosed fragment that does not parse
            "does not parse": '{"correctness": {"score": 5, "reason": "SECRET_FIXTURE"}, "faithfulness": {"sc',
            "rubric": json.dumps({**complete, "completeness": {"score": 9, "reason": "SECRET_FIXTURE"}}),
        }
        for reason, text in cases.items():
            with self.subTest(reason=reason):
                log = self.dropped(self.message(text, stop_reason="end_turn"))
                self.assertIn("judge vote dropped", log)
                self.assertIn(reason, log)
                self.assertIn("stop_reason=end_turn", log)
                self.assertNotIn("SECRET_FIXTURE", log)

    def test_a_reply_cut_at_max_tokens_says_how_to_fix_it(self):
        # The thinking alone reaches the limit and the reply stops with no text
        log = self.dropped(self.message(stop_reason="max_tokens", thinking=True))
        self.assertIn("stop_reason=max_tokens", log)
        self.assertIn("judge.max_tokens", log)
        self.assertIn("judge.effort", log)

    def test_a_refusal_reports_the_stop_details_without_the_explanation(self):
        details = types.SimpleNamespace(type="refusal", category="cyber", explanation="SECRET_FIXTURE")
        log = self.dropped(self.message(stop_reason="refusal", stop_details=details))
        self.assertIn("stop_reason=refusal", log)
        self.assertIn("cyber", log)
        self.assertNotIn("SECRET_FIXTURE", log)

    def test_a_reply_without_stop_fields_is_still_reported(self):
        # Even a reply without stop_reason (an older SDK or a fixture) reports the reason
        message = types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text="no json")])
        log = self.dropped(message)
        self.assertIn("no JSON", log)
        self.assertIn("stop_reason=None", log)


class JudgeRequestTests(unittest.TestCase):
    """The judge's max_tokens and effort. Effort is sent through output_config only when configured."""

    VOTE = json.dumps({axis: {"score": 5, "reason": "fixture"} for axis in AXES_FOR_TESTS})

    @classmethod
    def setUpClass(cls):
        cls.runner = load_eval_runner()

    def judge_params(self, cfg):
        message = types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text=self.VOTE)])
        create = Mock(return_value=message)
        client = types.SimpleNamespace(messages=types.SimpleNamespace(create=create))
        with patch.object(self.runner, "JUDGE_MODEL", "fixture-judge-model"):
            self.runner.eval_l2(client, {"id": "fixture", "category": "answer", "query": "fixture"}, {},
                                "rubric", {"votes": 1, **cfg})
        return create.call_args.kwargs

    def test_effort_is_sent_only_when_configured(self):
        self.assertNotIn("output_config", self.judge_params({}))
        for level in ("low", "medium", "high", "xhigh", "max"):
            with self.subTest(level=level):
                self.assertEqual(self.judge_params({"effort": level})["output_config"], {"effort": level})

    def test_max_tokens_without_a_configured_value_leaves_room_for_thinking(self):
        # Thinking counts toward max_tokens. 1024 cannot hold the thinking and the three axis reasons
        self.assertEqual(self.judge_params({})["max_tokens"], 16000)
        self.assertEqual(self.judge_params({"max_tokens": 8192})["max_tokens"], 8192)

    def test_invalid_effort_is_rejected(self):
        for bad in ("ultracode", "HIGH", "", True, 3, ["high"]):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "effort"):
                self.runner.judge_effort({"effort": bad})
        self.assertIsNone(self.runner.judge_effort({}))

    def test_invalid_effort_stops_before_evaluating(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cases.jsonl").write_text(json.dumps(
                {"id": "case", "category": "answer", "query": "fixture", "suite": ["smoke"]}))
            (root / "thresholds.json").write_text(json.dumps({
                "smoke": EvalGateTests.THRESHOLDS, "judge": {"votes": 1, "pass_score": 4, "effort": "extreme"}}))
            args = ["evals", "--dataset", str(root / "cases.jsonl"), "--thresholds",
                    str(root / "thresholds.json"), "--out", str(root / "out")]
            target = Mock(return_value={"answer": "ok"})
            with patch.object(sys, "argv", args), patch.object(self.runner, "call_target", target), \
                 patch.object(self.runner, "JUDGE_MODEL", "fixture-judge-model"), \
                 contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(ValueError, "effort"):
                self.runner.main()
            target.assert_not_called()
            self.assertFalse((root / "out").exists())

    def test_results_and_report_record_the_judge_model_with_its_effort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cases.jsonl").write_text(json.dumps(
                {"id": "case", "category": "answer", "query": "fixture", "suite": ["smoke"]}))
            for effort, expected in (("high", "high"), (None, None)):
                judge = {"votes": 1, "pass_score": 4, **({"effort": effort} if effort else {})}
                (root / "thresholds.json").write_text(json.dumps({"smoke": EvalGateTests.THRESHOLDS, "judge": judge}))
                args = ["evals", "--dataset", str(root / "cases.jsonl"), "--thresholds",
                        str(root / "thresholds.json"), "--out", str(root / "out")]
                scores = {axis: {"score": 5, "reason": "fixture"} for axis in AXES_FOR_TESTS}
                with self.subTest(effort=effort), patch.object(sys, "argv", args), \
                     patch.object(self.runner, "call_target", return_value={"answer": "ok"}), \
                     patch.object(self.runner, "eval_l2", return_value=scores), \
                     patch.object(self.runner, "JUDGE_MODEL", "fixture-judge-model"), \
                     contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(self.runner.main(), 0)
                    summary = json.loads((root / "out/results.json").read_text())["summary"]
                    # results.json alone pairs the judge model with its effort
                    self.assertEqual(summary["judge_model"], "fixture-judge-model")
                    self.assertEqual(summary["judge_effort"], expected)
                    report = (root / "out/report.md").read_text()
                    self.assertIn("fixture-judge-model", report)
                    self.assertIn(f"effort: {expected or 'API default'}", report)

    def test_shipped_judge_config_fits_a_non_streaming_call(self):
        # The SDK refuses a non-streaming call whose max_tokens exceeds about 21,333 before sending it
        judge = json.loads((ASSETS / "evals/thresholds.json").read_text())["judge"]
        self.assertGreaterEqual(judge["max_tokens"], 8192)
        self.assertLessEqual(judge["max_tokens"], 21333)
        # Effort is not sent by default (a judge on an older model that rejects effort does not get a 400)
        self.assertNotIn("effort", judge)


if __name__ == "__main__":
    unittest.main()
