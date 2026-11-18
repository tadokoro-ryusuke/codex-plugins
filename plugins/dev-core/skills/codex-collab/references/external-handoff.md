# Working From an External Handoff

Use this contract when another agent, another tool, or a person running an
orchestrator starts this Codex session to carry out one bounded assignment:
for example a parent in a different coding tool that launches Codex in a
terminal and points it at a handoff file. The assignment may be implementation,
review, design critique, or read-only research.

The handoff is the assignment. Follow its return format, write scope, and stop
conditions when it states them; apply the defaults below where it is silent.
If the handoff conflicts with a user instruction, an applicable `AGENTS.md`, or
a safety boundary, do not resolve the conflict by guessing: return `needs-parent`
with the conflicting passages.

## Recognize the situation

Treat the session as an external handoff when the first instruction asks you to
read a handoff file or contains a handoff with a role, a bounded outcome, and a
return format, and the requester owns the surrounding plan. A user asking you
to plan or execute their own work is not a handoff; use the normal entrypoints.

## Stay inside the assignment

- Do the one bounded outcome. Leave the overall plan, scope decisions,
  integration, and acceptance with the parent.
- Do not restart an orchestration workflow, start subagents or other agents, or
  hand the work to another model. If the selected reasoning mode starts
  subagents on its own, report that instead of proceeding.
- Write only inside the allowed write set. Treat every path outside it as
  read-only, including existing changes that belong to other work.
- A read-only role creates, modifies, and deletes nothing. The parent collects
  the final message; do not write a result file unless the handoff provides a
  writable path for it.
- Do not commit, push, open a pull request, publish, deploy, or write to shared
  services or data. These stay with the parent even when the write set includes
  deployment or release files: editing such a file is not permission to run it.
- Do not change dependencies or configuration outside the write set.
- Use the sandbox and approval settings the session was started with. Do not
  ask for broader access to finish faster; if the assignment cannot be met
  inside them, return `blocked`.

## Do the work

- For executable behavior or a regression fix, write the failing test first,
  then implement. Use applicable checks for other changes.
- Do not weaken an existing test (delete, skip, loosen an assertion, or
  special-case inputs) to make it pass. If a test cannot pass without that,
  stop and return the conflict.
- Other agents may share this machine. Limit how many builds and tests you run
  at once.
- Before returning, stop the background jobs you started and remove the
  temporary files you created.

## Return to the parent instead of guessing

Stop and return `needs-parent` with evidence when:

- the plan contradicts the code, or the specification and a test conflict;
- the work needs a public contract, data, or scope change the handoff does not
  include;
- the allowed write set cannot satisfy the acceptance criteria;
- the same fix path has failed three times.

Return `blocked` when a prerequisite, permission, tool, or environment is
missing, or when you decline part of the request. State exactly what was not
done.

## Return format

Use the handoff's format when it gives one. Otherwise end with a final message
in this shape. Repeat the dispatch identifier from the handoff so the parent can
match the result to the assignment. When the parent sends a correction with a
new attempt identifier, lead the new response with that identifier.

```text
Dispatch: <identifier from the handoff, or "none given">
Status: completed | needs-parent | blocked

Changed files            (implementation roles)
Findings                 (review roles: every finding, unfiltered, each with
                          P0-P3 severity, confidence, file:line, impact)
Commands run and results (exit codes; relevant output for failures)
Existing tests changed, skipped, or deleted, with the basis — or "none"
Checks not run, and why — or "none"
Problems encountered     (errors, workarounds, unresolved issues) — or "none"
Remaining concerns
```

Report every problem you hit, including ones you worked around and checks you
skipped. An empty "Problems encountered" section is a claim the parent will
verify against the diff and its own runs; an omitted failure costs more than a
reported one.

`completed` means the acceptance criteria in the handoff are met by evidence you
observed in this session. A budget or time limit reached is not `completed`:
record the remaining work and return the status that fits.
