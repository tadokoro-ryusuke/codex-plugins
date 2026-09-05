#!/usr/bin/env bash
# Six-step verification: build, types, lint, test, security, diff.
# Detects the project stack, runs whatever steps apply, and prints an
# evidence summary. Full logs are written to a temp directory so each
# claim can be backed by real command output.
#
# Usage: verify.sh [--skip step,step] [project-dir]
# Exit codes: 0 selected checks passed; 1 check failed; 2 incomplete/usage error.
# Detect manifests in project-dir only; use project workspace commands for nested packages.

set -u

SKIP=""
DIR="."
DIR_SET=0
usage_error() { echo "verify.sh: $1" >&2; exit 2; }
while [ $# -gt 0 ]; do
  case "$1" in
    --skip)
      [ $# -ge 2 ] && [ -n "$2" ] || usage_error "--skip requires a comma-separated step list"
      case ",$2," in *,,*) usage_error "empty --skip step" ;; esac
      IFS=',' read -r -a skip_steps <<< "$2"
      for step in "${skip_steps[@]}"; do
        case "$step" in build|types|lint|test|security|diff) ;; *) usage_error "unknown step: $step" ;; esac
      done
      SKIP="${SKIP},$2,"; shift 2 ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) usage_error "unknown option: $1" ;;
    *) [ "$DIR_SET" -eq 0 ] || usage_error "provide only one project directory"
       DIR="$1"; DIR_SET=1; shift ;;
  esac
done

cd "$DIR" || { echo "verify.sh: cannot cd to $DIR" >&2; exit 2; }

LOG_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify.XXXXXX")" || exit 2
FAILURES=0
BLOCKED=0
CHECKS=0
SUMMARY=""

note() { SUMMARY="${SUMMARY}$1\n"; }
is_skipped() { case "$SKIP" in *",${1%%:*},"*) return 0 ;; *) return 1 ;; esac; }
blocked_step() {
  if is_skipped "$1"; then note "SKIP  $1 (skipped by --skip)"; return; fi
  note "BLOCKED  $1 ($2)"
  BLOCKED=$((BLOCKED + 1))
}

# run_step <name> <command...>
# name may carry a stack suffix ("build:cargo"); --skip matches the base name.
run_step() {
  local name="$1"; shift
  local base="${name%%:*}"
  if is_skipped "$base"; then
    note "SKIP  $name (skipped by --skip)"
    return 0
  fi
  if [ $# -eq 0 ]; then
    note "SKIP  $name (no applicable command detected)"
    return 0
  fi
  if ! command -v "$1" >/dev/null 2>&1; then
    blocked_step "$name" "missing executable: $1; use the project-managed command"
    return
  fi
  local log="$LOG_DIR/$name.log"
  CHECKS=$((CHECKS + 1))
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

echo "== verification-loop: $(pwd) =="
echo "logs: $LOG_DIR"
if [ -n "$PM" ]; then
  if ! command -v node >/dev/null 2>&1; then
    blocked_step metadata:js "node is required to inspect package.json"
  elif ! node -e "JSON.parse(require('fs').readFileSync('package.json','utf8'))" >"$LOG_DIR/metadata:js.log" 2>&1; then
    blocked_step metadata:js "invalid package.json; see $LOG_DIR/metadata:js.log"
  fi
fi

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
elif [ -f tsconfig.json ]; then run_step types:js ./node_modules/.bin/tsc --noEmit; ran=1
fi
if [ -f pyproject.toml ]; then run_step types:py mypy .; ran=1; fi
[ "$ran" -eq 1 ] || run_step types

# --- Step 3: lint ---
ran=0
if [ -n "$PM" ] && has_npm_script lint; then run_step lint:js $PM run lint; ran=1; fi
if [ -f Cargo.toml ]; then run_step lint:cargo cargo clippy --all-targets -- -D warnings; ran=1; fi
if [ -f go.mod ]; then run_step lint:go go vet ./...; ran=1; fi
if [ -f pyproject.toml ]; then run_step lint:py ruff check .; ran=1; fi
[ "$ran" -eq 1 ] || run_step lint

# --- Step 4: test ---
ran=0
if [ -n "$PM" ] && has_npm_script test; then run_step test:js $PM run test; ran=1; fi
if [ -f Cargo.toml ]; then run_step test:cargo cargo test; ran=1; fi
if [ -f go.mod ]; then run_step test:go go test ./...; ran=1; fi
if [ -f pyproject.toml ]; then run_step test:py pytest -q; ran=1; fi
[ "$ran" -eq 1 ] || run_step test

# --- Step 5: security (dependency audit) ---
ran=0
if [ -n "$PM" ]; then
  case "$PM" in
    pnpm) run_step security:js pnpm audit --audit-level moderate ;;
    yarn|bun) blocked_step security:js "use the declared $PM version's project audit command" ;;
    npm) run_step security:js npm audit --audit-level=moderate ;;
  esac
  ran=1
fi
if [ -f Cargo.toml ]; then
  if command -v cargo-audit >/dev/null 2>&1; then run_step security:cargo cargo audit
  else blocked_step security:cargo "missing cargo-audit"; fi
  ran=1
fi
if [ -f go.mod ]; then run_step security:go govulncheck ./...; ran=1; fi
if [ -f pyproject.toml ]; then
  if [ -f requirements.txt ]; then run_step security:py pip-audit -r requirements.txt
  else blocked_step security:py "no requirements.txt; audit a project lock/export with the project command"; fi
  ran=1
fi
[ "$ran" -eq 1 ] || run_step security

# --- Step 6: diff (working tree state) ---
if is_skipped diff; then
  note "SKIP  diff (skipped by --skip)"
elif git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
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
if [ "$BLOCKED" -gt 0 ] || [ "$CHECKS" -eq 0 ]; then
  echo "RESULT: INCOMPLETE ($BLOCKED blocked step(s), $CHECKS executed check(s)); run project-specific checks"
  exit 2
fi
echo "RESULT: PASS (selected commands passed; assess listed skips and inspect the diff separately)"
