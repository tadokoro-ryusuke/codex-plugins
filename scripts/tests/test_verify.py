"""Exercise verify.sh through its CLI with an isolated PATH and fake toolchain."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


RUNNER = Path(__file__).resolve().parents[2] / "plugins/dev-core/skills/verification-loop/scripts/verify.sh"


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="verify-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        for name in ("bash", "mktemp", "tail", "sed", "node"):
            (self.bin / name).symlink_to(shutil.which(name))
        self.stub("git", "exit 1")
        self.env = {**os.environ, "PATH": str(self.bin), "TMPDIR": str(self.root),
                    "CALLS": str(self.root / "calls")}

    def stub(self, name, body='printf "%s\\n" "$0 $*" >> "$CALLS"\nexit 0'):
        path = self.bin / name
        path.write_text("#!/bin/bash\n" + body + "\n")
        path.chmod(0o755)

    def js(self):
        (self.project / "package.json").write_text(json.dumps({"scripts": {
            "build": "fake", "typecheck": "fake", "lint": "fake", "test": "fake"}}))
        self.stub("npm")

    def run_verify(self, *args):
        return subprocess.run(["/bin/bash", str(RUNNER), *args, str(self.project)],
                              env=self.env, text=True, capture_output=True, timeout=5)

    def test_missing_python_tools_are_visible_beside_passing_js(self):
        self.js()
        (self.project / "pyproject.toml").write_text("[project]\nname = 'fixture'\n")
        result = self.run_verify("--skip", "security")
        self.assertEqual(result.returncode, 2, result.stdout)
        for step in ("types:py", "lint:py", "test:py"):
            self.assertIn("BLOCKED  " + step, result.stdout)
        self.assertIn("PASS  test:js", result.stdout)

    def test_each_detected_stack_runs_and_failure_propagates(self):
        self.js()
        (self.project / "Cargo.toml").touch()
        self.stub("cargo", 'printf "%s\\n" "cargo $*" >> "$CALLS"\n[ "$1" != test ]')
        result = self.run_verify("--skip", "security")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("PASS  test:js", result.stdout)
        self.assertIn("FAIL  test:cargo", result.stdout)

    def test_python_audit_does_not_scan_unrelated_global_environment(self):
        self.js()
        (self.project / "pyproject.toml").touch()
        for name in ("mypy", "ruff", "pytest", "pip-audit"):
            self.stub(name)
        result = self.run_verify()
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("BLOCKED  security:py", result.stdout)
        self.assertNotIn("pip-audit", (self.root / "calls").read_text())

    def test_python_audit_uses_project_requirements(self):
        self.js()
        (self.project / "pyproject.toml").touch()
        (self.project / "requirements.txt").write_text("example-package==1.0\n")
        for name in ("mypy", "ruff", "pytest", "pip-audit"):
            self.stub(name)
        result = self.run_verify()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("pip-audit -r requirements.txt", (self.root / "calls").read_text())

    def test_no_workload_checks_is_incomplete(self):
        result = self.run_verify("--skip", "security")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("RESULT: INCOMPLETE", result.stdout)

    def test_bad_skip_does_not_run_project_commands(self):
        self.js()
        result = self.run_verify("--skip", "securty")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertFalse((self.root / "calls").exists())

    def test_missing_skip_value_exits_without_loop(self):
        result = subprocess.run(["/bin/bash", str(RUNNER), "--skip"], env=self.env,
                                text=True, capture_output=True, timeout=2)
        self.assertEqual(result.returncode, 2)

    def test_types_fallback_never_downloads_a_compiler(self):
        (self.project / "package.json").write_text('{"scripts":{"test":"fake"}}')
        (self.project / "tsconfig.json").touch()
        self.stub("npm")
        self.stub("npx")
        result = self.run_verify("--skip", "security")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("BLOCKED  types:js", result.stdout)
        self.assertNotIn("npx", (self.root / "calls").read_text())

    def test_explicit_skips_preserve_passing_selected_checks(self):
        self.js()
        (self.project / "pyproject.toml").touch()
        self.stub("pytest")
        result = self.run_verify("--skip", "types,lint,security,diff")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS  test:py", result.stdout)
        self.assertIn("SKIP  diff", result.stdout)


if __name__ == "__main__":
    unittest.main()
