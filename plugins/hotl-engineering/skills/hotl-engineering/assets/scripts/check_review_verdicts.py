#!/usr/bin/env python3
"""Validate required AI-review artifacts. Observe errors in Phase 1; enforce in Phase 2."""

import json
import os
from pathlib import Path
import re


def main():
    errors = []
    critical = 0
    expected_sha = os.environ.get("EXPECTED_SHA", "")
    tier2 = os.environ.get("TIER2", "")
    if os.environ.get("IS_DRAFT") == "true":
        print("SKIP: draft PR; review is required when ready")
        return 0
    if os.environ.get("CLASSIFY_RESULT") != "success" or tier2 not in ("true", "false"):
        errors.append("classification missing or unsuccessful")
    if not re.fullmatch(r"[0-9a-f]{40}", expected_sha):
        errors.append("expected PR revision missing or invalid")
    tiers = [("light", "REVIEW_RESULT")]
    if tier2 == "true":
        tiers.append(("deep", "DEEP_RESULT"))
    root = Path(os.environ.get("VERDICT_DIR", "verdicts"))
    for tier, result_key in tiers:
        if os.environ.get(result_key) != "success":
            errors.append(f"{tier}: job did not succeed")
        path = root / f"ai-review-verdict-{tier}" / "verdict.json"
        try:
            verdict = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(verdict, dict):
                raise ValueError("expected a JSON object")
            for field in ("critical", "high"):
                if type(verdict.get(field)) is not int or verdict[field] < 0:
                    raise ValueError(f"{field} must be a nonnegative integer")
            if verdict.get("head_sha") != expected_sha:
                raise ValueError("verdict does not match the PR revision")
            critical += verdict["critical"]
        except (OSError, ValueError) as error:
            errors.append(f"{tier}: missing or invalid verdict ({type(error).__name__})")
    if critical:
        errors.append(f"{critical} CRITICAL finding(s)")
    enforce = os.environ.get("ENFORCE") == "true"
    if errors:
        print("INCOMPLETE/FAIL: " + "; ".join(errors))
        print("Enforcement enabled" if enforce else "Observation only; this is not approval evidence")
    else:
        print(f"PASS: validated {len(tiers)} required verdict(s) for {expected_sha}")
    return 1 if errors and enforce else 0


if __name__ == "__main__":
    raise SystemExit(main())
