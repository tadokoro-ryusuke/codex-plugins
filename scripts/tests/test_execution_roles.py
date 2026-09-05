"""Exercise role resolution through its command-line interface."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
RESOLVER = (
    ROOT
    / "plugins/dev-core/skills/codex-collab/scripts/resolve_execution_role.py"
)


class ExecutionRoleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="execution-role-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.capabilities = self.write_json(
            "capabilities.json",
            {
                "can_select_model": True,
                "can_select_effort": True,
                "models": {
                    "gpt-5.6-sol": ["low", "medium", "high"],
                    "gpt-6-astra": ["medium", "high", "xhigh"],
                },
            },
        )
        self.profile = self.write_json(
            "profile.json",
            {
                "schema_version": 1,
                "parent_recommendation": {
                    "model": "gpt-6-astra",
                    "reasoning_effort": "high",
                },
                "roles": {
                    "implementer": {
                        "model": "gpt-5.6-sol",
                        "reasoning_effort": "medium",
                        "write_policy": "scoped-write",
                    },
                    "reviewer": {
                        "model": "gpt-6-astra",
                        "reasoning_effort": "high",
                        "write_policy": "read-only",
                    },
                },
            },
        )

    def write_json(self, name, value):
        path = self.directory / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_resolver(self, *arguments, cwd=None):
        return subprocess.run(
            ["python3", str(RESOLVER), *arguments],
            cwd=cwd or self.directory,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def assert_rejected(self, result):
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.strip())

    def test_implementer_defaults_resolve_to_spawn_request(self):
        result = self.run_resolver(
            "--role",
            "implementer",
            "--capabilities",
            str(self.capabilities),
            "--profile",
            str(self.profile),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "role": "implementer",
                "model": "gpt-5.6-sol",
                "reasoning_effort": "medium",
                "write_policy": "scoped-write",
                "fork_turns": "none",
            },
        )

    def test_reviewer_defaults_and_default_profile_are_script_relative(self):
        unrelated_cwd = self.directory / "unrelated" / "working-directory"
        unrelated_cwd.mkdir(parents=True)
        result = self.run_resolver(
            "--role",
            "reviewer",
            "--capabilities",
            str(self.capabilities),
            cwd=unrelated_cwd,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["model"], "gpt-6-astra")
        self.assertEqual(json.loads(result.stdout)["reasoning_effort"], "high")
        self.assertEqual(json.loads(result.stdout)["write_policy"], "read-only")

    def test_complete_explicit_override_is_validated_and_used(self):
        result = self.run_resolver(
            "--role",
            "implementer",
            "--capabilities",
            str(self.capabilities),
            "--profile",
            str(self.profile),
            "--model",
            "gpt-6-astra",
            "--effort",
            "xhigh",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual((output["model"], output["reasoning_effort"]),
                         ("gpt-6-astra", "xhigh"))
        self.assertEqual(output["write_policy"], "scoped-write")

    def test_model_override_preserves_reviewer_read_only_policy(self):
        result = self.run_resolver(
            "--role",
            "reviewer",
            "--capabilities",
            str(self.capabilities),
            "--profile",
            str(self.profile),
            "--model",
            "gpt-5.6-sol",
            "--effort",
            "medium",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual((output["model"], output["reasoning_effort"]),
                         ("gpt-5.6-sol", "medium"))
        self.assertEqual(output["write_policy"], "read-only")

    def test_partial_override_and_unknown_role_are_rejected(self):
        common = ["--capabilities", str(self.capabilities), "--profile", str(self.profile)]
        for arguments in (
            ["--role", "implementer", *common, "--model", "gpt-6-astra"],
            ["--role", "implementer", *common, "--effort", "high"],
            ["--role", "operator", *common],
        ):
            with self.subTest(arguments=arguments):
                self.assert_rejected(self.run_resolver(*arguments))

    def test_unavailable_model_or_effort_never_falls_back(self):
        unsupported = self.write_json(
            "unsupported.json",
            {
                "can_select_model": True,
                "can_select_effort": True,
                "models": {"gpt-5.6-sol": ["low"]},
            },
        )
        for arguments in (
            ["--role", "reviewer", "--capabilities", str(unsupported),
             "--profile", str(self.profile)],
            ["--role", "implementer", "--capabilities", str(self.capabilities),
             "--profile", str(self.profile), "--model", "gpt-6-astra",
             "--effort", "ultra"],
        ):
            with self.subTest(arguments=arguments):
                self.assert_rejected(self.run_resolver(*arguments))

    def test_false_selectors_and_invalid_capability_types_are_rejected(self):
        invalid_documents = (
            {"can_select_model": False, "can_select_effort": True, "models": {}},
            {"can_select_model": True, "can_select_effort": False, "models": {}},
            {"can_select_model": "yes", "can_select_effort": True, "models": {}},
            {"can_select_model": True, "can_select_effort": True, "models": []},
            {"can_select_model": True, "can_select_effort": True,
             "models": {"gpt-5.6-sol": "medium"}},
            {"can_select_model": True, "can_select_effort": True,
             "models": {"gpt-5.6-sol": ["medium", 1]}},
        )
        for index, document in enumerate(invalid_documents):
            with self.subTest(document=document):
                path = self.write_json(f"bad-capabilities-{index}.json", document)
                self.assert_rejected(
                    self.run_resolver("--role", "implementer", "--capabilities", str(path),
                                      "--profile", str(self.profile))
                )

    def test_malformed_json_and_missing_files_are_rejected(self):
        malformed = self.directory / "malformed.json"
        malformed.write_text("{not json", encoding="utf-8")
        missing = self.directory / "missing.json"
        for capabilities, profile in (
            (malformed, self.profile),
            (self.capabilities, malformed),
            (missing, self.profile),
            (self.capabilities, missing),
        ):
            with self.subTest(capabilities=capabilities, profile=profile):
                self.assert_rejected(
                    self.run_resolver("--role", "implementer",
                                      "--capabilities", str(capabilities),
                                      "--profile", str(profile))
                )

    def test_invalid_profile_shapes_and_values_are_rejected(self):
        invalid_documents = (
            [],
            {"schema_version": 2, "parent_recommendation": {}, "roles": {}},
            {"schema_version": 1, "parent_recommendation": {}, "roles": []},
            {"schema_version": 1,
             "parent_recommendation": {"model": "gpt-6-astra", "reasoning_effort": "high"},
             "roles": {"implementer": {"model": "gpt-5.6-sol",
                                         "reasoning_effort": "medium"}}},
            {"schema_version": 1,
             "parent_recommendation": {"model": 6, "reasoning_effort": "high"},
             "roles": {"implementer": {"model": "gpt-5.6-sol",
                                         "reasoning_effort": "medium",
                                         "write_policy": "scoped-write"}}},
        )
        for index, document in enumerate(invalid_documents):
            with self.subTest(document=document):
                path = self.write_json(f"bad-profile-{index}.json", document)
                self.assert_rejected(
                    self.run_resolver("--role", "implementer",
                                      "--capabilities", str(self.capabilities),
                                      "--profile", str(path))
                )

    def test_role_write_policy_cannot_expand_or_swap_ownership(self):
        for role_name, invalid_policy in (
            ("implementer", "read-only"),
            ("reviewer", "scoped-write"),
            ("reviewer", "arbitrary-policy"),
        ):
            with self.subTest(role=role_name, policy=invalid_policy):
                profile = json.loads(self.profile.read_text(encoding="utf-8"))
                profile["roles"][role_name]["write_policy"] = invalid_policy
                path = self.write_json(
                    f"bad-{role_name}-{invalid_policy}.json", profile
                )
                self.assert_rejected(
                    self.run_resolver("--role", role_name,
                                      "--capabilities", str(self.capabilities),
                                      "--profile", str(path))
                )

    def test_whitespace_only_profile_and_capability_values_are_rejected(self):
        whitespace_profile = json.loads(self.profile.read_text(encoding="utf-8"))
        whitespace_profile["roles"]["implementer"]["model"] = "   "
        profile_path = self.write_json("whitespace-profile.json", whitespace_profile)
        capabilities_with_whitespace_model = self.write_json(
            "whitespace-model-capabilities.json",
            {
                "can_select_model": True,
                "can_select_effort": True,
                "models": {
                    "   ": ["medium"],
                    "gpt-5.6-sol": ["medium"],
                    "gpt-6-astra": ["high"],
                },
            },
        )
        capabilities_with_whitespace_effort = self.write_json(
            "whitespace-effort-capabilities.json",
            {
                "can_select_model": True,
                "can_select_effort": True,
                "models": {
                    "gpt-5.6-sol": ["medium", "   "],
                    "gpt-6-astra": ["high"],
                },
            },
        )

        cases = (
            (profile_path, capabilities_with_whitespace_model),
            (self.profile, capabilities_with_whitespace_model),
            (self.profile, capabilities_with_whitespace_effort),
        )
        for profile, capabilities in cases:
            with self.subTest(profile=profile, capabilities=capabilities):
                self.assert_rejected(
                    self.run_resolver("--role", "implementer",
                                      "--capabilities", str(capabilities),
                                      "--profile", str(profile))
                )

    def test_required_arguments_are_rejected_by_cli(self):
        for arguments in (
            ["--capabilities", str(self.capabilities)],
            ["--role", "implementer"],
        ):
            with self.subTest(arguments=arguments):
                self.assert_rejected(self.run_resolver(*arguments))


if __name__ == "__main__":
    unittest.main()
