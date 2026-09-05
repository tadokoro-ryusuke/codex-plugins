---
name: verification-loop
description: "Verify coding changes with current evidence from project build, type, lint, test, security, and diff checks. Use to validate work, prepare a PR, or assess completion; includes a fallback runner for common stacks."
---

# Verification Loop

Choose checks that prove the requested change. Inspect AGENTS.md, CI, manifests,
lockfiles, and existing project commands before running a generic command.
Keep required repository gates. Run focused checks first, then broaden for the
touched contracts and risks. Do not repeat a completed suite without a new
change, failure, or unresolved concern.

## Choose evidence

Consider build, types, lint/format, tests, security, and diff review. Mark a
category not applicable with a reason when appropriate; do not fabricate a
test merely to mirror a low-impact prose change. Preserve test-first development
for executable behavior and regression fixes.

Use the project's package manager and environment. Prefer configured workspace
commands for monorepos, Tauri, Workers, or mixed stacks. Run each affected
package if the root command does not cover it. Do not silently install a missing
compiler, audit the global Python environment, or guess a deploy command.

## Optional fallback runner

Resolve this path relative to the skill directory:

```bash
scripts/verify.sh [--skip step,step] [project-dir]
```

Use it only when its commands match the project. It detects manifests in the
specified directory, runs each detected stack, and writes per-step logs to a
temporary directory. It does not recursively discover packages or establish
browser/device/deployment behavior. `diff` reports working-tree state; inspect
the actual diff and run `git diff --check` separately.

| Result | Meaning | Next action |
| --- | --- | --- |
| PASS | Executed command returned success | Check that its scope supports the claim |
| FAIL | Executed command failed | Inspect the log and fix a verified in-scope cause |
| BLOCKED | Detected step lacks a prerequisite or a reliable generic command | Use a project-managed equivalent; disclose any remaining gap |
| SKIP | Explicitly excluded or no generic command detected | Explain applicability; a skip is not success |

Exit codes: `0` means selected commands passed with no blocked step; `1` means a
command failed; `2` means incomplete verification or invalid arguments. No
workload checks also returns `2`. Explicit `--skip` accepts only `build`, `types`,
`lint`, `test`, `security`, and `diff`; it does not waive a required project gate.

Python fallback uses mypy, Ruff, and pytest from PATH. If the project uses uv,
Poetry, a virtual environment, or another checker, run its configured commands.
Python audit requires a project requirements file; other locks need their own
export/audit procedure. Yarn/Bun audit requires a version-appropriate project
command rather than borrowing npm's audit. Security commands may access advisory
services or resolve dependencies; respect the task's network constraints.

## Evidence-based completion

Support new completion claims with output inspected in this turn and relevant
to the final code. Record command, working directory, exit status, revision/diff
identity, and artifact path. After a relevant edit, re-run the affected checks.
Retain earlier results as history, not current proof.

- Build output proves that build in its environment.
- A test proves the assertions it executes, not an unobserved integration.
- Dependency audit output covers known advisories for its input; never translate
  it into a claim that the system has no vulnerabilities.
- Local browser/device observations and deployed behavior need separate evidence.
- Coverage is a diagnostic signal. Follow configured thresholds; do not impose
  a universal percentage or weaken a gate to make a result green.

Report executed checks, skips with reasons, relevant review findings, and the
remaining evidence gaps. Summarize routine passing output; link logs when they
help assess a failure. Do not copy sample counts or expose secrets/customer data.
