#!/usr/bin/env python3
"""PreToolUse hook: deny destructive shell commands.

Reads the hook payload from stdin and emits a permissionDecision JSON
response. Anything that doesn't match the deny list is allowed through
silently (exit 0, no output).
"""

import json
import re
import sys

DENY_PATTERNS = [
    (r"rm\s+(-[a-zA-Z]*[rf][a-zA-Z]*\s+)+[\"']?(~/?|/\*?)[\"']?(\s|$)", "rm -rf on / or ~"),
    (r"\bdrop\s+(table|database)\b", "DROP TABLE/DATABASE"),
    (r"\btruncate\s+table\b", "TRUNCATE TABLE"),
    (r"git\s+push\s+(--force|-f)\s+(origin\s+)?(main|master)\b", "force-push to main/master"),
    (r"git\s+reset\s+--hard\b", "git reset --hard"),
    (r"git\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed payload: never block on hook errors

    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if isinstance(command, list):
        command = " ".join(str(part) for part in command)
    if not isinstance(command, str):
        return 0

    for pattern, label in DENY_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"dev-core hook blocked a destructive command ({label}). "
                        "If this is intentional, run it manually outside the agent."
                    ),
                }
            }))
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
