#!/usr/bin/env python3
"""Prepare and grade the bounded execution smoke fixture.

This utility checks a task's behavior and edit boundary. It is not a security
sandbox and does not verify the effective model used by an agent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


ASSET_DIRECTORY = Path(__file__).resolve().parent.parent / "assets" / "execution-smoke"
ASSERTION_HELPER = ASSET_DIRECTORY / "behavioral_assertions.py"
FIXTURE_FILES = (
    Path("totals.py"),
    Path("test_totals.py"),
    Path("AGENTS.md"),
    Path("docs/plans/task-line-total.md"),
)
ALLOWED_CHANGES = {
    "totals.py",
    "test_totals.py",
    "docs/plans/task-line-total.md",
}
BASELINE_SCHEMA = 1
BEHAVIOR_TIMEOUT_SECONDS = 2
BEHAVIOR_TEST_COUNT = 5
COMPLETION_PREFIX = "EXECUTION_SMOKE_COMPLETION="


class PreconditionError(Exception):
    """Raised when a fixture cannot be prepared or graded."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_git(directory: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=directory,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "unknown Git error"
        raise PreconditionError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def run_prepare_git(directory: Path, *args: str) -> str:
    return run_git(
        directory,
        "-c",
        "commit.gpgSign=false",
        "-c",
        f"core.hooksPath={os.devnull}",
        *args,
    )


def baseline_path(directory: Path) -> Path:
    return Path(f"{directory}.baseline.json")


def emit(report: dict[str, Any]) -> None:
    print(json.dumps(report, sort_keys=True))


def prepare(directory: Path) -> int:
    directory = directory.expanduser().resolve()
    baseline = baseline_path(directory)
    if directory.exists():
        raise PreconditionError(f"target already exists: {directory}")
    if baseline.exists():
        raise PreconditionError(f"baseline already exists: {baseline}")
    if not ASSERTION_HELPER.is_file():
        raise PreconditionError(f"bundled assertion helper is missing: {ASSERTION_HELPER}")

    directory.mkdir(parents=True)
    try:
        for relative in FIXTURE_FILES:
            source = ASSET_DIRECTORY / relative
            if not source.is_file():
                raise PreconditionError(f"fixture asset is missing: {source}")
            destination = directory / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

        run_prepare_git(directory, "init", "--quiet")
        run_prepare_git(
            directory, "add", "--", *(path.as_posix() for path in FIXTURE_FILES)
        )
        run_prepare_git(
            directory,
            "-c",
            "user.name=Execution Fixture",
            "-c",
            "user.email=execution-fixture@example.com",
            "commit",
            "--quiet",
            "-m",
            "Initialize execution smoke fixture",
        )
        revision = run_git(directory, "rev-parse", "HEAD")
        baseline_data = {
            "schema_version": BASELINE_SCHEMA,
            "directory": str(directory),
            "initial_revision": revision,
            "files": {
                relative.as_posix(): sha256_file(directory / relative)
                for relative in FIXTURE_FILES
            },
        }
        baseline.write_text(
            json.dumps(baseline_data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except Exception:
        if baseline.exists():
            baseline.unlink()
        shutil.rmtree(directory)
        raise

    emit(
        {
            "status": "prepared",
            "directory": str(directory),
            "baseline": str(baseline),
            "initial_revision": revision,
        }
    )
    return 0


def load_baseline(directory: Path) -> tuple[Path, dict[str, Any]]:
    baseline = baseline_path(directory)
    if not directory.is_dir():
        raise PreconditionError(f"fixture directory is missing: {directory}")
    if not baseline.is_file():
        raise PreconditionError(f"baseline is missing: {baseline}")
    try:
        data = json.loads(baseline.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PreconditionError(f"baseline is unreadable: {error}") from error
    if not isinstance(data, dict):
        raise PreconditionError("baseline root must be a JSON object")
    schema_version = data.get("schema_version")
    if type(schema_version) is not int or schema_version != BASELINE_SCHEMA:
        raise PreconditionError("baseline schema is unsupported")
    if not isinstance(data.get("directory"), str) or data["directory"] != str(directory):
        raise PreconditionError("baseline belongs to a different fixture directory")
    files = data.get("files")
    revision = data.get("initial_revision")
    if not isinstance(revision, str) or not isinstance(files, dict):
        raise PreconditionError("baseline is incomplete")
    if re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision) is None:
        raise PreconditionError("baseline revision is invalid")
    if set(files) != {path.as_posix() for path in FIXTURE_FILES} or not all(
        isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest)
        for digest in files.values()
    ):
        raise PreconditionError("baseline file inventory is invalid")
    return baseline, data


def is_generated_artifact(relative: Path) -> bool:
    parts = relative.parts
    return "__pycache__" in parts and relative.suffix in {".pyc", ".pyo"}


def inspect_scope(
    directory: Path,
    baseline: dict[str, Any],
    *,
    missing_is_precondition: bool,
) -> list[str]:
    errors: list[str] = []
    git_directory = directory / ".git"
    git_is_valid = True
    if git_directory.is_symlink():
        errors.append("unexpected symlink: .git")
        git_is_valid = False
    elif not git_directory.is_dir():
        if missing_is_precondition:
            raise PreconditionError("fixture Git directory is missing")
        errors.append("fixture Git directory is missing")
        git_is_valid = False

    for relative in FIXTURE_FILES:
        candidate = directory / relative
        if candidate.is_symlink():
            continue
        if not candidate.is_file():
            message = f"required fixture file is missing: {relative}"
            if missing_is_precondition:
                raise PreconditionError(message)
            errors.append(message)

    if git_is_valid:
        revision = run_git(directory, "rev-parse", "HEAD")
        remotes = run_git(directory, "remote")
        if revision != baseline["initial_revision"]:
            errors.append("initial Git revision changed")
        if remotes:
            errors.append("Git remotes were added")

    expected_files = set(baseline["files"])
    actual_files: set[str] = set()
    symlinks: set[str] = set()
    for path in directory.rglob("*"):
        relative = path.relative_to(directory)
        if relative.parts and relative.parts[0] == ".git":
            continue
        if path.is_symlink():
            symlinks.add(relative.as_posix())
            errors.append(f"unexpected symlink: {relative.as_posix()}")
            actual_files.add(relative.as_posix())
            continue
        if path.is_dir():
            continue
        if is_generated_artifact(relative):
            continue
        actual_files.add(relative.as_posix())

    for relative in sorted(actual_files - expected_files):
        if relative not in ALLOWED_CHANGES:
            errors.append(relative)
    for relative in sorted(expected_files - actual_files):
        errors.append(f"missing tracked fixture file: {relative}")

    for relative, expected_hash in baseline["files"].items():
        if (
            relative in ALLOWED_CHANGES
            or relative not in actual_files
            or relative in symlinks
        ):
            continue
        if sha256_file(directory / relative) != expected_hash:
            errors.append(relative)
    return errors


def run_behavior(directory: Path) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        sys.executable,
        str(ASSERTION_HELPER),
        "--directory",
        str(directory),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=directory,
            env=environment,
            text=True,
            capture_output=True,
            timeout=BEHAVIOR_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        stdout = (
            error.stdout.decode(errors="replace")
            if isinstance(error.stdout, bytes)
            else error.stdout
        )
        stderr = (
            error.stderr.decode(errors="replace")
            if isinstance(error.stderr, bytes)
            else error.stderr
        )
        return {
            "passed": False,
            "timed_out": True,
            "timeout_seconds": BEHAVIOR_TIMEOUT_SECONDS,
            "stdout": stdout or "",
            "stderr": stderr or "candidate behavior timed out",
            "error": "candidate behavior timed out",
        }
    completion_reports: list[Any] = []
    for line in completed.stdout.splitlines():
        if not line.startswith(COMPLETION_PREFIX):
            continue
        try:
            completion_reports.append(json.loads(line.removeprefix(COMPLETION_PREFIX)))
        except json.JSONDecodeError:
            completion_reports.append(None)
    expected_completion = {
        "schema_version": 1,
        "tests_run": BEHAVIOR_TEST_COUNT,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "successful": True,
    }
    completion_valid = completion_reports == [expected_completion]
    passed = completed.returncode == 0 and completion_valid
    if not completion_valid:
        error = "fixed behavioral assertion completion report is missing or invalid"
    elif completed.returncode != 0:
        error = "behavioral assertions failed"
    else:
        error = None
    return {
        "passed": passed,
        "timed_out": False,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "completion": completion_reports[0] if len(completion_reports) == 1 else None,
        "error": error,
    }


def grade(directory: Path) -> int:
    directory = directory.expanduser().resolve()
    _baseline_file, baseline = load_baseline(directory)
    scope_errors = inspect_scope(directory, baseline, missing_is_precondition=True)
    if scope_errors:
        report = {
            "status": "failed",
            "checks": {"behavior": "not_run", "scope": "failed"},
            "scope_errors": scope_errors,
            "behavior": None,
        }
        emit(report)
        return 1

    behavior = run_behavior(directory)
    try:
        scope_errors = inspect_scope(
            directory, baseline, missing_is_precondition=False
        )
    except PreconditionError as error:
        scope_errors = [f"post-behavior scope check failed: {error}"]
    behavior_passed = behavior["passed"]
    scope_passed = not scope_errors
    passed = behavior_passed and scope_passed
    emit(
        {
            "status": "passed" if passed else "failed",
            "checks": {
                "behavior": "passed" if behavior_passed else "failed",
                "scope": "passed" if scope_passed else "failed",
            },
            "scope_errors": scope_errors,
            "behavior": behavior,
        }
    )
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare or grade the bounded native-agent execution fixture."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "grade"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--directory", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            return prepare(args.directory)
        return grade(args.directory)
    except PreconditionError as error:
        emit({"status": "incomplete", "error": str(error)})
        return 2
    except (OSError, subprocess.SubprocessError) as error:
        emit({"status": "incomplete", "error": str(error)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
