---
name: verification-loop
description: "Verify changed software using project checks when assessing completion or delivery readiness."
---

# Verification Loop

Choose checks that prove the requested change. Use applicable project instructions
and existing commands; consult CI, manifests, or lockfiles when command selection
or environment details are unclear.
Keep required repository gates. Run focused checks first, then broaden for the
touched contracts and risks. Executable behavior changes also need the full-suite
completion gate below before completion or commit. Do not repeat a completed suite
without a new change, failure, or unresolved concern.

## Choose evidence

Consider build, types, lint/format, tests, security, and diff review. Mark a
category not applicable with a reason when appropriate; do not fabricate a
test merely to mirror a low-impact prose change. Preserve test-first development
for executable behavior and regression fixes.

Use the project's package manager and environment. Prefer configured workspace
commands for monorepos, Tauri, Workers, or mixed stacks. Run each affected
package if the root command does not cover it. Do not silently install a missing
compiler, audit the global Python environment, or guess a deploy command.

## Tests and test weakening

A passing test step counts only when selection, skips, or deletions did not shrink
the suite it claims to cover. A test that passed only on retry is not pass evidence;
report it as flaky, and report flaky/retry counts when the runner prints them.

During diff review, check for changes that weaken tests:

- added focus or skip markers (`.only`, `fit`, `fdescribe`, `.skip`, `xit`,
  `@pytest.mark.skip`, `t.Skip()`, `#[ignore]`, `@Disabled`, and similar)
- deleted or renamed test files
- a net reduction in `expect`/`assert` lines
- bulk updates of snapshot or approval files
- loosened coverage thresholds or test exclusion settings (`testPathIgnorePatterns`
  and similar)

For each hit, report its basis: a specification change or, for a skip, an approved
quarantine that meets `$test-design`'s conditions (owner, expiry, tracked failure,
replacement coverage for critical paths). Do not mark tests or the final result as
passing while a hit has neither basis. Use
`$test-design` for flake quarantine rules and `$conventions-as-guardrails` for
runner and linter settings that block focus/skip markers deterministically.

## Dependency audit results

A dependency audit gate means the configured audit command passes at its configured
threshold with its approved exclusions (`$cicd-release-design` owns the threshold and
exception policy). Some tools apply the threshold only to the exit code and still
print lower-severity findings (for example, `npm audit --audit-level`). Report the
gate result (command, threshold, exit code, exclusions applied with reason and expiry)
separately from the findings printed, including those below the threshold. When the
gate passes, write "no findings at or above <threshold>", never "no known
vulnerabilities" or "no vulnerabilities".

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
services or resolve dependencies; respect the task's network constraints. The
runner's npm/pnpm audit uses `moderate` as a generic fallback; the project's
configured audit command and threshold govern the gate.

## Evidence-based completion

Support completion claims with output inspected now and relevant to the final
code. Record command, working directory, exit status, execution time,
revision/diff identity, relevant environment, and artifact path.

Reuse a prior result only when its raw artifact is available, the relevant source,
tests, dependencies, configuration, and environment still match, and project
rules permit reuse. Label it as a prior execution inspected now, not a new run.
Run affected checks when those inputs changed, their identity cannot be verified,
an unresolved concern remains, or a fresh run is required. Time-sensitive or live
system checks need current observations. A summary saying "passed" is insufficient.

- Build output proves that build in its environment.
- A test proves the assertions it executes, not an unobserved integration. A
  focused green is not a suite green.
- Dependency audit output covers the advisories its tool knows for its input. Cite
  the command, threshold, exit code, and exclusions with reason and expiry; a bare
  "audit clean" without them is not evidence. Never translate a passing gate into
  a claim that the system has no vulnerabilities.
- Local browser/device observations and deployed behavior need separate evidence.
- Coverage is a diagnostic signal. Follow configured thresholds; do not impose
  a universal percentage or weaken a gate to make a result green.

Report executed checks, skips with reasons, relevant review findings, and the
remaining evidence gaps. Summarize routine passing output; link logs when they
help assess a failure. Do not copy sample counts or expose secrets/customer data.

## Full-suite completion gate

This is the single definition of the gate; other dev-core skills point here.
Before claiming completion of, or committing, an executable behavior change
(feature, regression or bug fix, or refactor), the owner who claims completion
needs a passing unfiltered run of the project's test command for the final input.
Run it once, or reuse an earlier full-suite result only under the reuse rules in
"Evidence-based completion" above. A focused or targeted-file green does not meet
this gate.

- Not run (skipped, unavailable, or unable to start): do not claim completion or
  commit; report it as blocked or not run with the reason.
- Failed: do not claim completion or commit. Name every failure, including ones the
  change did not cause, with any evidence that a failure predates the change, and
  leave acceptance pending for the owner's decision.

A delegated unit may return focused evidence; its parent meets this gate at the
final gate. A deliberately partial request, such as writing only a failing Red
test, is exempt. Prose-only changes with no executable behavior are outside it.
