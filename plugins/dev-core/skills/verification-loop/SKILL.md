---
name: verification-loop
description: "Evidence-based 6-step verification: build, typecheck, lint, test, security audit, and diff review, with a bundled runner script. Use when asked to verify changes, finish a coding task, prepare a PR, prove that checks pass, or when claiming work is done."
---

# Verification Loop

Run all six steps and report with evidence. Never declare a step passed without command output from this turn.

## Run the bundled script first

```bash
scripts/verify.sh [--skip step,step] [project-dir]
```

(Resolve the path relative to this skill directory.)

The script detects the stack (npm/pnpm/yarn/bun scripts, Cargo, Go, Python), runs build → types → lint → test → security → diff, writes full logs to a temp directory, and prints a PASS/FAIL/SKIP summary. Exit code 0 means no applicable step failed.

After running:

1. Quote the summary block in your report.
2. For every FAIL, read the step's log file, fix the cause, and re-run.
3. For every SKIP, decide whether the step truly doesn't apply (e.g. no test runner configured). If it should apply, run the project's own command manually and report that output.

The script only knows common stacks. When the project defines its own verification commands (Makefile, CI config, AGENTS.md), prefer those and report their output instead.

## Iron Law: evidence-based completion

A claim requires same-turn command output. Cached results, previous runs, and "should pass" reasoning are not evidence.

| Claim | Required evidence | Not evidence |
|---|---|---|
| Build succeeds | This turn's build output, exit 0 | "My change doesn't affect the build" |
| No type errors | This turn's typecheck output | "I fixed the types" |
| Lint passes | This turn's lint output | "It passed last time" |
| All tests pass | This turn's test run, 0 failures | "Untouched code, should pass" |
| No vulnerabilities | This turn's audit output | "I didn't change dependencies" |

Red flags that violate the rule: "should pass", "probably fine", "passed previously", "no impact since nothing changed", or any checkmark without attached output.

## Report format

```
[Verification]
PASS  build    (pnpm run build)
PASS  types    (pnpm run typecheck)
WARN  lint     (3 warnings)
PASS  test     (pnpm run test, coverage 85%)
PASS  security (npm audit)
WARN  diff     (uncommitted changes)

[Action needed]
- Fix lint warnings: pnpm lint --fix
```

Coverage target when measurable: 80%+. New behavior must come with tests (see $dev-tdd).
