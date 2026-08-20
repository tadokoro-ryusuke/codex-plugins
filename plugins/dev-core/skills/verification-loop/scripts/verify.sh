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
# name may carry a stack suffix ("build:cargo"); --skip matches the base name.
run_step() {
  local name="$1"; shift
  local base="${name%%:*}"
  if [ -n "$SKIP" ] && [ "${SKIP#*,"$base",}" != "$SKIP" ]; then
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

# Each step runs for EVERY detected stack, not just the first match.
# A multi-manifest repo (Tauri = package.json + Cargo.toml, Python + JS
# monorepos) must verify all of its languages; first-match-only would
# silently drop one side and report a false PASS.

# --- Step 1: build ---
ran=0
if [ -n "$PM" ] && has_npm_script build; then run_step build:js $PM run build; ran=1; fi
if [ -f Cargo.toml ]; then run_step build:cargo cargo build --all-targets; ran=1; fi
if [ -f go.mod ]; then run_step build:go go build ./...; ran=1; fi
[ "$ran" -eq 1 ] || run_step build

# --- Step 2: types ---
ran=0
if [ -n "$PM" ] && has_npm_script typecheck; then run_step types:js $PM run typecheck; ran=1
elif [ -f tsconfig.json ]; then run_step types:js npx tsc --noEmit; ran=1
fi
if [ -f pyproject.toml ] && command -v mypy >/dev/null 2>&1; then run_step types:py mypy .; ran=1; fi
[ "$ran" -eq 1 ] || run_step types

# --- Step 3: lint ---
ran=0
if [ -n "$PM" ] && has_npm_script lint; then run_step lint:js $PM run lint; ran=1; fi
if [ -f Cargo.toml ]; then run_step lint:cargo cargo clippy --all-targets -- -D warnings; ran=1; fi
if [ -f go.mod ]; then run_step lint:go go vet ./...; ran=1; fi
if [ -f pyproject.toml ] && command -v ruff >/dev/null 2>&1; then run_step lint:py ruff check .; ran=1; fi
[ "$ran" -eq 1 ] || run_step lint

# --- Step 4: test ---
ran=0
if [ -n "$PM" ] && has_npm_script test; then run_step test:js $PM run test; ran=1; fi
if [ -f Cargo.toml ]; then run_step test:cargo cargo test; ran=1; fi
if [ -f go.mod ]; then run_step test:go go test ./...; ran=1; fi
if [ -f pyproject.toml ] && command -v pytest >/dev/null 2>&1; then run_step test:py pytest -q; ran=1; fi
[ "$ran" -eq 1 ] || run_step test

# --- Step 5: security (dependency audit) ---
ran=0
if [ -n "$PM" ]; then
  case "$PM" in
    pnpm) run_step security:js pnpm audit --audit-level moderate ;;
    yarn) run_step security:js yarn npm audit --severity moderate ;;
    *) run_step security:js npm audit --audit-level=moderate ;;
  esac
  ran=1
fi
if [ -f Cargo.toml ] && command -v cargo-audit >/dev/null 2>&1; then run_step security:cargo cargo audit; ran=1; fi
if [ -f pyproject.toml ] && command -v pip-audit >/dev/null 2>&1; then run_step security:py pip-audit; ran=1; fi
[ "$ran" -eq 1 ] || run_step security

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
