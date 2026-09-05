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

    def run_evals(self, cases, target, judge=None, revision=None, missing_baseline=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cases.jsonl").write_text("\n".join(json.dumps(c) for c in cases))
            (root / "thresholds.json").write_text(json.dumps({"smoke": {
                "must_pass_rate": 1, "must_not_violations": 0, "judge_total_floor": 10}}))
            args = ["evals", "--dataset", str(root / "cases.jsonl"), "--thresholds",
                    str(root / "thresholds.json"), "--out", str(root / "out")]
            if revision:
                args += ["--expected-revision", revision]
            if missing_baseline:
                args += ["--baseline", str(root / "missing-baseline.json")]
            scores = {axis: {"score": 5, "reason": "fixture"} for axis in self.runner.AXES}
            with patch.object(sys, "argv", args), patch.object(self.runner, "call_target", side_effect=target), \
                 patch.object(self.runner, "eval_l2", side_effect=judge, return_value=scores), \
                 contextlib.redirect_stdout(io.StringIO()):
                result = self.runner.main()
            return result, json.loads((root / "out/results.json").read_text())

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


if __name__ == "__main__":
    unittest.main()
