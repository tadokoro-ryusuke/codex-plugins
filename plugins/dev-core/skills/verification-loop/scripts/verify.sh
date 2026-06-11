#!/usr/bin/env bash
# Six-step verification: build, types, lint, test, security, diff.
# Detects the project stack, runs whatever steps apply, and prints an
# evidence summary. Full logs are written to a temp directory so each
# claim can be backed by real command output.
#
# Usage: verify.sh [--skip step,step] [project-dir]
# Exit code: 0 only if no applicable step failed (skipped steps don't fail).

set -u

SKIP=""
DIR="."
while [ $# -gt 0 ]; do
  case "$1" in
    --skip) SKIP=",$2,"; shift 2 ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) DIR="$1"; shift ;;
  esac
done

cd "$DIR" || { echo "verify.sh: cannot cd to $DIR" >&2; exit 2; }

LOG_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify.XXXXXX")"
FAILURES=0
SUMMARY=""

note() { SUMMARY="${SUMMARY}$1\n"; }

# run_step <name> <command...>
run_step() {
  local name="$1"; shift
  if [ -n "$SKIP" ] && [ "${SKIP#*,"$name",}" != "$SKIP" ]; then
    note "SKIP  $name (skipped by --skip)"
    return 0
  fi
  if [ $# -eq 0 ]; then
    note "SKIP  $name (no applicable command detected)"
    return 0
  fi
  local log="$LOG_DIR/$name.log"
  if "$@" >"$log" 2>&1; then
    note "PASS  $name ($*)  log: $log"
  else
    note "FAIL  $name ($*)  exit=$?  log: $log"
    tail -n 20 "$log" | sed "s/^/  [$name] /"
    FAILURES=$((FAILURES + 1))
  fi
}

# has_npm_script <name> — true if package.json defines the script
has_npm_script() {
  [ -f package.json ] && command -v node >/dev/null 2>&1 &&
    node -e "process.exit(require('./package.json').scripts?.['$1'] ? 0 : 1)" 2>/dev/null
}

# Detect package manager for JS projects.
PM=""
if [ -f package.json ]; then
  if [ -f pnpm-lock.yaml ]; then PM="pnpm"
  elif [ -f yarn.lock ]; then PM="yarn"
  elif [ -f bun.lockb ] || [ -f bun.lock ]; then PM="bun"
  else PM="npm"
  fi
fi

js_cmd() { # js_cmd <script-name> — echoes "<pm> run <script>" if defined
  has_npm_script "$1" && echo "$PM run $1"
}

echo "== verification-loop: $(pwd) =="
echo "logs: $LOG_DIR"

# --- Step 1: build ---
if [ -n "$PM" ] && has_npm_script build; then run_step build $PM run build
elif [ -f Cargo.toml ]; then run_step build cargo build --all-targets
elif [ -f go.mod ]; then run_step build go build ./...
else run_step build
fi

# --- Step 2: types ---
if [ -n "$PM" ] && has_npm_script typecheck; then run_step types $PM run typecheck
elif [ -f tsconfig.json ]; then run_step types npx tsc --noEmit
elif [ -f pyproject.toml ] && command -v mypy >/dev/null 2>&1; then run_step types mypy .
else run_step types
fi

# --- Step 3: lint ---
if [ -n "$PM" ] && has_npm_script lint; then run_step lint $PM run lint
elif [ -f Cargo.toml ]; then run_step lint cargo clippy --all-targets -- -D warnings
elif [ -f go.mod ]; then run_step lint go vet ./...
elif [ -f pyproject.toml ] && command -v ruff >/dev/null 2>&1; then run_step lint ruff check .
else run_step lint
fi

# --- Step 4: test ---
if [ -n "$PM" ] && has_npm_script test; then run_step test $PM run test
elif [ -f Cargo.toml ]; then run_step test cargo test
elif [ -f go.mod ]; then run_step test go test ./...
elif [ -f pyproject.toml ] && command -v pytest >/dev/null 2>&1; then run_step test pytest -q
else run_step test
fi

# --- Step 5: security (dependency audit) ---
if [ -n "$PM" ]; then
  case "$PM" in
    pnpm) run_step security pnpm audit --audit-level moderate ;;
    yarn) run_step security yarn npm audit --severity moderate ;;
    *) run_step security npm audit --audit-level=moderate ;;
  esac
elif [ -f Cargo.toml ] && command -v cargo-audit >/dev/null 2>&1; then run_step security cargo audit
elif [ -f pyproject.toml ] && command -v pip-audit >/dev/null 2>&1; then run_step security pip-audit
else run_step security
fi

# --- Step 6: diff (working tree state) ---
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  {
    echo "--- git status ---"
    git status --short
    echo "--- diff stat vs HEAD ---"
    git diff --stat HEAD
  } >"$LOG_DIR/diff.log" 2>&1
  if [ -n "$(git status --porcelain)" ]; then
    note "WARN  diff (uncommitted changes present)  log: $LOG_DIR/diff.log"
  else
    note "PASS  diff (working tree clean)  log: $LOG_DIR/diff.log"
  fi
else
  note "SKIP  diff (not a git repository)"
fi

echo
printf "%b" "$SUMMARY"
echo
if [ "$FAILURES" -gt 0 ]; then
  echo "RESULT: FAIL ($FAILURES step(s) failed)"
  exit 1
fi
echo "RESULT: PASS (skipped steps are listed above; confirm they don't apply)"
