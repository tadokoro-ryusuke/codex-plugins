#!/usr/bin/env bash
# SessionStart hook: stdout becomes extra developer context for the session.
# Keep the output short — it is paid for on every session start.

set -u

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[dev-core] Repository state:"
  branch="$(git branch --show-current 2>/dev/null)"
  echo "- branch: ${branch:-detached}"
  dirty="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  echo "- uncommitted changes: ${dirty} file(s)"
  echo "- recent commits:"
  git log --oneline -3 2>/dev/null | sed 's/^/    /'

  plans="$(ls docs/plans/task-*.md 2>/dev/null | head -5)"
  if [ -n "$plans" ]; then
    echo "- open plan documents (consider resuming with \$dev-execute):"
    echo "$plans" | sed 's/^/    /'
  fi
fi

cat <<'EOF'
[dev-core] Session discipline:
- Iron Law: no production code without a test; never claim a check passed without running it this turn.
- No rationalizing skipped checks ("small change", "passed before").
- Independently verify subagent claims before relying on them.
- Three Strikes: after 3 failed fix attempts, stop and report to the user.
EOF
