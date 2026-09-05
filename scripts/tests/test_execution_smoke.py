from __future__ import annotations

import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / "plugins"
    / "dev-core"
    / "skills"
    / "codex-collab"
    / "scripts"
    / "execution_smoke.py"
)


CORRECT_IMPLEMENTATION = """
def total_cents(lines):
    total = 0
    for line in lines:
        quantity = line.get("quantity", 1)
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        total += line["unit_price_cents"] * quantity
    return total
"""


WRONG_IMPLEMENTATION = """
def total_cents(lines):
    return sum(line["unit_price_cents"] * line.get("quantity", 1) for line in lines)
"""


class ExecutionSmokeCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fixture = Path(self.temp.name) / "fixture"

    def run_cli(
        self,
        *args: str,
        timeout: float = 10,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
            env=environment,
        )

    def prepare(self) -> dict[str, object]:
        result = self.run_cli("prepare", "--directory", str(self.fixture))
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        return json.loads(result.stdout)

    def grade(
        self, timeout: float = 10
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        result = self.run_cli("grade", "--directory", str(self.fixture), timeout=timeout)
        return result, json.loads(result.stdout)

    def write_totals(self, source: str) -> None:
        (self.fixture / "totals.py").write_text(
            textwrap.dedent(source).lstrip(), encoding="utf-8"
        )

    def test_prepare_creates_committed_fixture_and_external_baseline(self) -> None:
        report = self.prepare()

        self.assertEqual(report["status"], "prepared")
        self.assertTrue((self.fixture / ".git").is_dir())
        self.assertTrue((self.fixture / "totals.py").is_file())
        self.assertTrue((self.fixture / "test_totals.py").is_file())
        self.assertTrue((self.fixture / "AGENTS.md").is_file())
        self.assertTrue((self.fixture / "docs/plans/task-line-total.md").is_file())
        baseline = Path(f"{self.fixture}.baseline.json")
        self.assertTrue(baseline.is_file())

        remotes = subprocess.run(
            ["git", "remote"], cwd=self.fixture, text=True, capture_output=True, check=True
        )
        self.assertEqual(remotes.stdout, "")
        initial_tests = subprocess.run(
            [sys.executable, "-m", "unittest", "-v"],
            cwd=self.fixture,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(initial_tests.returncode, 0, initial_tests.stderr)

    def test_prepare_rejects_preexisting_target_or_baseline(self) -> None:
        self.fixture.mkdir()
        result = self.run_cli("prepare", "--directory", str(self.fixture))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "incomplete")

        self.fixture.rmdir()
        Path(f"{self.fixture}.baseline.json").write_text("{}", encoding="utf-8")
        result = self.run_cli("prepare", "--directory", str(self.fixture))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.fixture.exists())

    def test_prepare_disables_inherited_signing_and_hooks(self) -> None:
        global_config = Path(self.temp.name) / "synthetic-global.gitconfig"
        hooks = Path(self.temp.name) / "inherited-hooks"
        hooks.mkdir()
        sentinel = Path(self.temp.name) / "hook-ran"
        pre_commit = hooks / "pre-commit"
        pre_commit.write_text(
            f"#!/bin/sh\ntouch {sentinel}\nexit 1\n",
            encoding="utf-8",
        )
        pre_commit.chmod(0o755)
        global_config.write_text(
            textwrap.dedent(
                f"""
                [commit]
                    gpgSign = true
                [gpg]
                    program = /usr/bin/false
                [core]
                    hooksPath = {hooks}
                """
            ),
            encoding="utf-8",
        )
        environment = os.environ.copy()
        environment["GIT_CONFIG_GLOBAL"] = str(global_config)
        environment["GIT_CONFIG_NOSYSTEM"] = "1"

        result = self.run_cli(
            "prepare",
            "--directory",
            str(self.fixture),
            environment=environment,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertFalse(sentinel.exists())

    def test_unchanged_candidate_fails_behavioral_grade(self) -> None:
        self.prepare()
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["checks"]["behavior"], "failed")
        self.assertIn("quantity", report["behavior"]["stderr"])

    def test_exit_zero_without_assertion_completion_fails(self) -> None:
        self.prepare()
        self.write_totals("raise SystemExit(0)")
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["checks"]["behavior"], "failed")
        self.assertIn("completion report", report["behavior"]["error"])

    def test_correct_candidate_passes(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        result, report = self.grade()

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["checks"], {"behavior": "passed", "scope": "passed"})

    def test_candidate_tests_cannot_mask_wrong_behavior(self) -> None:
        self.prepare()
        self.write_totals(WRONG_IMPLEMENTATION)
        (self.fixture / "test_totals.py").write_text(
            "import unittest\n\nclass AlwaysPasses(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n",
            encoding="utf-8",
        )
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["checks"]["behavior"], "failed")

    def test_stale_bytecode_cannot_mask_wrong_final_source(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        source = self.fixture / "totals.py"
        original_stat = source.stat()
        py_compile.compile(
            str(source),
            doraise=True,
            invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
        )
        correct_source = source.read_text(encoding="utf-8")
        wrong_source = correct_source.replace("* quantity", "+ quantity")
        self.assertEqual(len(wrong_source), len(correct_source))
        source.write_text(wrong_source, encoding="utf-8")
        os.utime(
            source,
            ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns),
        )
        self.assertTrue(any((self.fixture / "__pycache__").glob("totals.*.pyc")))

        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["checks"]["behavior"], "failed")

    def test_scope_escape_new_file_fails(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        (self.fixture / "notes.txt").write_text("out of scope\n", encoding="utf-8")
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["checks"]["scope"], "failed")
        self.assertIn("notes.txt", report["scope_errors"])

    def test_changed_instructions_fail(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        (self.fixture / "AGENTS.md").write_text("changed\n", encoding="utf-8")
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertIn("AGENTS.md", report["scope_errors"])

    def test_runtime_scope_mutation_fails_after_behavior(self) -> None:
        self.prepare()
        self.write_totals(
            CORRECT_IMPLEMENTATION
            + textwrap.dedent(
                """

                from pathlib import Path
                _original_total_cents = total_cents

                def total_cents(lines):
                    Path("AGENTS.md").write_text("changed during grade\\n", encoding="utf-8")
                    Path("runtime-note.txt").write_text("created during grade\\n", encoding="utf-8")
                    return _original_total_cents(lines)
                """
            )
        )
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["checks"]["behavior"], "passed")
        self.assertEqual(report["checks"]["scope"], "failed")
        self.assertIn("AGENTS.md", report["scope_errors"])
        self.assertIn("runtime-note.txt", report["scope_errors"])

    def test_changed_baseline_commit_fails(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture Candidate",
                "-c",
                "user.email=fixture-candidate@example.com",
                "add",
                "totals.py",
            ],
            cwd=self.fixture,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture Candidate",
                "-c",
                "user.email=fixture-candidate@example.com",
                "commit",
                "-m",
                "candidate commit",
            ],
            cwd=self.fixture,
            text=True,
            capture_output=True,
            check=True,
        )
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertIn("initial Git revision", " ".join(report["scope_errors"]))

    def test_added_remote_fails(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        subprocess.run(
            ["git", "remote", "add", "origin", "https://example.com/fixture.git"],
            cwd=self.fixture,
            check=True,
        )
        result, report = self.grade()

        self.assertEqual(result.returncode, 1)
        self.assertIn("Git remotes were added", report["scope_errors"])

    def test_hanging_candidate_times_out_and_fails(self) -> None:
        self.prepare()
        self.write_totals(
            """
            def total_cents(lines):
                while True:
                    pass
            """
        )
        result, report = self.grade(timeout=8)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["checks"]["behavior"], "failed")
        self.assertTrue(report["behavior"]["timed_out"])

    def test_invalid_baseline_shapes_are_incomplete(self) -> None:
        self.prepare()
        baseline_path = Path(f"{self.fixture}.baseline.json")
        valid = json.loads(baseline_path.read_text(encoding="utf-8"))
        invalid_baselines = (
            [],
            1,
            "baseline",
            {**valid, "schema_version": True},
            {**valid, "initial_revision": "not-a-revision"},
            {**valid, "files": []},
            {**valid, "files": {**valid["files"], "AGENTS.md": 123}},
        )

        for invalid in invalid_baselines:
            with self.subTest(invalid=invalid):
                baseline_path.write_text(json.dumps(invalid), encoding="utf-8")
                result = self.run_cli("grade", "--directory", str(self.fixture))
                self.assertEqual(result.returncode, 2, result.stderr or result.stdout)
                self.assertEqual(json.loads(result.stdout)["status"], "incomplete")

    def test_directory_and_git_symlinks_fail_scope(self) -> None:
        self.prepare()
        self.write_totals(CORRECT_IMPLEMENTATION)
        linked = self.fixture / "linked-docs"
        linked.symlink_to(self.fixture / "docs", target_is_directory=True)
        result, report = self.grade()
        self.assertEqual(result.returncode, 1)
        self.assertIn("linked-docs", " ".join(report["scope_errors"]))

        linked.unlink()
        git_directory = self.fixture / ".git"
        moved_git_directory = self.fixture / ".fixture-git"
        git_directory.rename(moved_git_directory)
        git_directory.symlink_to(moved_git_directory, target_is_directory=True)
        result, report = self.grade()
        self.assertEqual(result.returncode, 1)
        self.assertIn(".git", " ".join(report["scope_errors"]))


if __name__ == "__main__":
    unittest.main()
