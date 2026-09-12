# Tooling and hooks

Reuse the project's formatter, linter, type checker, and task runner. Adopt existing
rules before introducing another tool. For a new repository, choose the smallest
set that enforces its actual contracts; optional editor or commit hooks should not
become a prerequisite to every task.

For architecture rules, state the intended dependency boundary in one sentence,
then encode it with the language's existing tooling. Add a violating example that
must fail and a legitimate dependency that must pass. Start with the boundary
that matters; do not add a new layer layout to make the test possible. Generate
actual dependency graphs when inspecting imports, and distinguish them from a
conceptual architecture diagram.

## Agent hooks

Use hooks for cheap, targeted feedback where the runtime supports them. Bound their
runtime and affected files. Avoid running the full build/test suite after every
edit; retain appropriate completion and CI checks for the final revision.

Check the runtime's supported events, payload, response format, timeout, and trust
requirements before writing a handler. Verify representative payloads and failure
paths. Keep deny rules scoped to the real operation and permission boundary;
a text match or generic shell ban is not proof that the intended policy is enforced.

A suppression must be narrow, justified, and visible in review. Preserve repository
requirements for approval, but do not manufacture a new approval stop for every
comment when the task already authorizes that routine repair. Waiving a required
gate or widening privileged access remains a separate owner decision.

Keep local and CI commands reproducible. Record actual enforcement evidence rather
than asserting that a local check has already blocked a remote PR. Do not deliberately
break or mutate a live remote system just to demonstrate the gate.
