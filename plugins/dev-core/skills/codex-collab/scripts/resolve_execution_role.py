#!/usr/bin/env python3
"""Resolve a requested execution role against caller-observed capabilities."""

import argparse
import json
from pathlib import Path
import sys
from typing import Any


DEFAULT_PROFILE = Path(__file__).resolve().parent.parent / "assets/execution-profile.json"
ROLE_NAMES = ("implementer", "reviewer")
ROLE_WRITE_POLICIES = {
    "implementer": "scoped-write",
    "reviewer": "read-only",
}


class InputError(ValueError):
    """Report an invalid caller-supplied document or selection."""


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"error: {message}\n")


def parse_arguments() -> argparse.Namespace:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=ROLE_NAMES, required=True)
    parser.add_argument("--capabilities", type=Path, required=True)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--model")
    parser.add_argument("--effort")
    arguments = parser.parse_args()
    if (arguments.model is None) != (arguments.effort is None):
        parser.error("--model and --effort must be provided together")
    return arguments


def load_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InputError(f"cannot read {label}: {error}") from error


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputError(f"{label} must be an object")
    return value


def require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} must be a non-empty string")
    return value


def validate_profile(value: Any) -> dict[str, Any]:
    profile = require_object(value, "profile")
    if type(profile.get("schema_version")) is not int or profile["schema_version"] != 1:
        raise InputError("profile schema_version must be 1")

    parent = require_object(profile.get("parent_recommendation"),
                            "profile parent_recommendation")
    require_nonempty_string(parent.get("model"), "parent recommendation model")
    require_nonempty_string(parent.get("reasoning_effort"),
                            "parent recommendation reasoning_effort")

    roles = require_object(profile.get("roles"), "profile roles")
    for role_name in ROLE_NAMES:
        role = require_object(roles.get(role_name), f"profile role {role_name}")
        require_nonempty_string(role.get("model"), f"{role_name} model")
        require_nonempty_string(role.get("reasoning_effort"),
                                f"{role_name} reasoning_effort")
        write_policy = require_nonempty_string(
            role.get("write_policy"), f"{role_name} write_policy"
        )
        if write_policy != ROLE_WRITE_POLICIES[role_name]:
            raise InputError(
                f"{role_name} write_policy must be "
                f"{ROLE_WRITE_POLICIES[role_name]}"
            )
    return profile


def validate_capabilities(value: Any) -> dict[str, list[str]]:
    capabilities = require_object(value, "capabilities")
    for selector in ("can_select_model", "can_select_effort"):
        if type(capabilities.get(selector)) is not bool:
            raise InputError(f"capabilities {selector} must be a boolean")
        if not capabilities[selector]:
            raise InputError(f"capabilities {selector} must be true")

    models = require_object(capabilities.get("models"), "capabilities models")
    validated: dict[str, list[str]] = {}
    for model, efforts in models.items():
        model_name = require_nonempty_string(model, "capabilities model name")
        if not isinstance(efforts, list):
            raise InputError(f"capabilities efforts for {model_name} must be an array")
        validated_efforts = []
        for effort in efforts:
            validated_efforts.append(
                require_nonempty_string(effort, f"capabilities effort for {model_name}")
            )
        validated[model_name] = validated_efforts
    return validated


def resolve(arguments: argparse.Namespace) -> dict[str, str]:
    profile = validate_profile(load_json(arguments.profile, "profile"))
    capabilities = validate_capabilities(
        load_json(arguments.capabilities, "capabilities")
    )
    role = profile["roles"][arguments.role]
    model = arguments.model if arguments.model is not None else role["model"]
    effort = (
        arguments.effort
        if arguments.effort is not None
        else role["reasoning_effort"]
    )

    if model not in capabilities:
        raise InputError(f"model is unavailable: {model}")
    if effort not in capabilities[model]:
        raise InputError(f"effort is unavailable for {model}: {effort}")

    return {
        "role": arguments.role,
        "model": model,
        "reasoning_effort": effort,
        "write_policy": role["write_policy"],
        "fork_turns": "none",
    }


def main() -> int:
    arguments = parse_arguments()
    try:
        result = resolve(arguments)
    except InputError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
