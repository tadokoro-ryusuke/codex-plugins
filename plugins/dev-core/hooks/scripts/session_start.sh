#!/usr/bin/env bash
# SessionStart hook: emits Codex hook JSON; additionalContext becomes extra
# developer context for the session.
# Keep the context short — it is paid for on every session start.
#
# NOTE: Codex treats stdout starting with '{' or '[' as JSON and rejects it if
# it fails to parse (codex-rs/hooks output_parser::looks_like_json). Plain text
# starting with "[dev-core]" therefore breaks; always emit the JSON envelope.

set -u

collect_context() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[dev-core] Repository state:"
    branch="$(git branch --show-current 2>/dev/null)"
    safe_branch="$(printf '%s' "${branch:-detached}" | LC_ALL=C tr -cd 'A-Za-z0-9._/-' | cut -c1-120)"
    echo "- branch: ${safe_branch:-detached}"
    dirty="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
    echo "- uncommitted changes: ${dirty} file(s)"
    commit_hashes="$(git rev-list --max-count=3 --abbrev-commit HEAD 2>/dev/null | paste -sd ' ' -)"
    if [ -n "$commit_hashes" ]; then
      echo "- recent commit ids: $commit_hashes"
    fi

    plan_state="$(
      find docs/plans -maxdepth 1 -type f -name 'task-*.md' 2>/dev/null \
        | sort \
        | while IFS= read -r plan; do
            status="$(sed -n 's/^- Status:[[:space:]]*//p' "$plan" | head -1)"
            if [ "$status" = "done" ]; then
              continue
            fi
            if [ "$status" != "draft" ] && [ "$status" != "approved" ] \
              && [ "$status" != "in-progress" ] && [ "$status" != "blocked" ]; then
              continue
            fi
            safe_plan="$(printf '%s' "$plan" | LC_ALL=C tr -cd 'A-Za-z0-9._/-' | cut -c1-160)"
            [ -n "$safe_plan" ] || continue
            printf '    %s [status: %s]\n' "$safe_plan" "$status"
          done \
        | head -10
    )"
    if [ -n "$plan_state" ]; then
      echo "- resumable plans (open the plan before using \$dev-execute):"
      echo "$plan_state"
    fi
  fi

  cat <<'EOF'
[dev-core] Session discipline:
- Iron Law: no production code without a test; never claim a check passed without running it this turn.
- No rationalizing skipped checks ("small change", "passed before").
- Independently verify subagent claims before relying on them.
- Keep plan progress, decisions, evidence, and the current next action durable across context resets.
- Three Strikes: after 3 failed fix attempts, stop and report to the user.
EOF
}

collect_context | python3 -c '
import json
import sys

text = sys.stdin.read().strip()
output = {}
if text:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": text,
        }
    }
print(json.dumps(output))
'
