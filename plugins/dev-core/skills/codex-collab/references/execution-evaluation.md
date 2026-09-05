# Evaluate Role-Based Execution

Use this procedure to exercise the actual parent/implementation/review workflow
after instruction changes. Keep deterministic policy/fixture tests separate from
native model behavior, effective-model metadata, and general quality claims.

## Prepare a bounded case

From the collaboration skill directory, prepare a new temporary workspace:

```bash
python3 scripts/execution_smoke.py prepare --directory "$fixture_dir"
```

Choose a directory that does not exist. The helper seeds a small Python repository
and an approved plan, plus an external baseline used by its grader. Keep the
baseline and grader outside the candidate agent's authorized write set. A
temporary working directory is not an OS security sandbox; use the host's
available restrictions and the fixture's explicit no-network/no-publishing scope.

Capture the plugin revision, capability observations, requested parent model and
effort, fixture path, and baseline identity. Record effective runtime settings
only when the host exposes them. Keep raw tool traces private; publish only a
minimal sanitized result record.

## Run with native agents

Start a fresh coordinating agent with this realistic request, substituting paths:

```text
Use $dev-execute at <source skill path> to implement the approved plan in
<fixture>/docs/plans/task-line-total.md. Work only in that fixture and follow
its AGENTS.md. Use the role-based implementation and independent-review workflow.
Complete the plan, verify the result, and report the evidence.
```

Provide the applicable skills and allowed fixture scope, but keep evaluator
expectations and the independent grader out of the task prompt. Let the updated
skill determine role assignment. Do not supply an implementation or expected
review verdict. Use the current host's model and concurrency capabilities; avoid
using nested user-owned tasks as a substitute for native subagents.

Explicitly permit read-only access to the supplied source skills and a separately
prepared capability file; keep writes inside the fixture's allowed set. This tiny
case explicitly requests role delegation. It does not test the heuristic for
deciding whether an otherwise small task deserves delegation.

Inspect native dispatch records to determine whether an implementation agent and
a separate reviewer were requested with the resolved settings and fresh context.
Check ownership, parent decisions, child return evidence, and the stable revision
or diff reviewed. A task that merely says it used those roles has not supplied
dispatch evidence.

## Grade independently

After the agents have stopped writing, run:

```bash
python3 scripts/execution_smoke.py grade --directory "$fixture_dir"
```

The grader checks the final behavior with parent-owned assertions and checks its
fixture scope/baseline. It does not trust candidate-written tests as its oracle,
start a model, attest backend model selection, or prove the absence of side
effects outside the observed fixture. Inspect task traces for those boundaries.

Report these dimensions separately:

| Dimension | Evidence |
| --- | --- |
| Requested routing | Actual spawn arguments and returned agent IDs |
| Effective routing | Runtime-reported model/effort, or `unverified` |
| Behavior | Independent grader output plus relevant task checks |
| Scope and review | File/command evidence and separate review dispatch |
| Efficiency | Elapsed time, correction rounds, and usage when observable |

Do not turn missing effective-model metadata into success or infer it from an
agent's self-report. One passing case is a smoke result, not a measured general
success rate. Keep the broader cases in the dev-core evaluation suite pending
until executed. For comparisons, run representative cases with the same inputs
before/after changes and repeat them before making quality or cost claims.
