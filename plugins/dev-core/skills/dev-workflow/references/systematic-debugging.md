# Systematic Debugging

Use this for bugs, errors, failing tests, flakes, performance regressions, and production-like incidents.

## Iron Rule

Do not fix before root-cause investigation. A quick patch without a confirmed cause is not done.

## Four Phases

### 1. Collect

- Actual symptom and expected behavior.
- Reproduction steps.
- Full error message and stack trace.
- Recent changes from `git log --oneline -10`, `git diff`, or PR context.
- Affected files, modules, and data paths.
- Frequency and environment.

### 2. Hypothesize

Write three independent hypotheses. For each:

- What would be true if this hypothesis is correct.
- How to test it.
- Which files or logs matter.

### 3. Verify

- Look for supporting and contradicting evidence.
- Eliminate hypotheses explicitly.
- If all are eliminated, return to collection.
- Do not edit until one root cause is confirmed or the user asks for an exploratory patch.

### 4. Fix

- Add a regression test when practical.
- Make the smallest root-cause fix.
- Run focused verification first, then broader checks.
- Capture the lesson with `continuous-learning` when the pattern can recur.

## Three Strikes Rule

After three failed fix attempts:

1. Stop.
2. List each attempt and why it failed.
3. Explain the suspected misunderstanding.
4. Switch to `codex-collab` rescue workflow or ask for user direction.

