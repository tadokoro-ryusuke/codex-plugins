# Systematic Debugging

Use this for bugs, errors, failing tests, flakes, performance regressions, and production-like incidents.

## Iron Rule

Do not fix before root-cause investigation. A quick patch without a confirmed cause is not done.

## Four Phases

### 1. Collect

- Actual symptom and expected behavior.
- A reproduction command that judges the symptom itself: a test, a `curl` call, a
  CLI run with a fixture. Make it as deterministic, fast, and unattended as you can.
- Full error message and stack trace.
- Recent changes from `git log --oneline -10`, `git diff`, or PR context.
- Affected files, modules, and data paths.
- Frequency and environment.

Collection is complete only when you have run the reproduction command at least
once and its actual output shows the symptom (red). Do not move to hypotheses
before that. Redact secrets in any output you show.

- For intermittent failures, raise the reproduction rate with repeated runs and by
  fixing time, randomness, and execution order.
- If you cannot build a reproduction command, list what you tried and stop. Ask
  for access to an environment that reproduces it, redacted logs or artifacts, or
  permission for temporary instrumentation. Do not proceed to hypotheses on guesses.
- Once it reproduces, remove one element at a time and rerun to reach a minimal
  reproduction. For a regression between a known good and bad revision, automate
  the search with `git bisect run`, on a clean working tree or in a separate worktree.

### 2. Hypothesize

Form competing hypotheses that could explain the symptom, usually two or three.
Start with the strongest explanation; propose only one when the evidence leaves no
competing explanation, and state why the alternatives were dismissed. For each:

- A falsifiable prediction: "if X causes it, changing Y produces Z".
- How to test it.
- Which files or logs matter.

### 3. Verify

- Look for supporting and contradicting evidence.
- Eliminate hypotheses explicitly.
- If all are eliminated, return to collection.
- Do not edit until one root cause is confirmed or the user asks for an exploratory patch.
- Tag temporary investigation logging with a unique marker and, before finishing,
  search for the marker to confirm none remains.

### 4. Fix

- If the fix is within the request, fix it test-first: turn the reproduction into a
  failing regression test, then make the smallest root-cause fix. If the request is
  diagnosis only, report the root cause and fix plan and stop.
- When no suitable seam exists for a regression test, report that as a finding.
- Run focused verification; broaden only for affected shared behavior or unresolved risk.
- Capture the lesson with `continuous-learning` when the pattern can recur.

## Three Strikes Rule

After three similar failed fixes on the same failing path:

1. Stop that path; continue independent authorized work.
2. List each attempt and why it failed.
3. Explain the suspected misunderstanding and recommend the next step.
4. Switch to a fresh in-session diagnosis (the `codex-collab` rescue workflow) or
   ask for user direction. Hand the rescue to another agent or model only with the
   user's consent or prior authorization in the plan or request; when that
   authorization covers diagnosis only, request read-only work.

Preserve the attempt history across agent or owner changes. Separate failures
with different causes and expected test-first failures from repeated failed fixes.
