# Evaluate Execution Decisions and Delegation

Use this procedure after delegation or instruction changes. Separate packaging
validation, deterministic helper tests, native skill behavior, and comparative
quality/cost evidence. Do not treat compliance with the old topology as the goal.

## Choose the evaluation question

- Use the existing smoke below to check explicitly requested dispatch, ownership,
  and evidence. It does not measure the decision to delegate.
- Use realistic requests without a delegation instruction to test that decision.
  Include a large sequential change, independent source investigations, low-risk
  prose changes, and parent implementation requiring an independent reviewer.
- Test unavailable optional dispatch separately from unavailable explicit model
  requirements or required review. Exercise unchanged/stale check artifacts,
  different failure causes, repeated same-path failures, and cancelled writers.
- Test discovery in clean sessions with direct, paraphrased, and non-matching
  requests. Refine descriptions for misrouting and the workflow for bad outcomes
  after correct activation. Do not expose the expected verdicts to the candidate.

Use `../../../evals/skill-behavior-cases.json` as the behavioral case inventory.
Keep cases pending until a model actually executes them; schema checks only
validate their structure.

## Compare execution arrangements

Use matched temporary fixtures and fresh sessions for these comparison arms:

| Arm | Ownership |
| --- | --- |
| Parent | Parent implementation and self-review |
| Parent + reviewer | Parent implementation and a fresh independent reviewer |
| Delegated | Bounded implementation child and a fresh reviewer; parent integrates |

Compare the old and revised policy on the same unhinted requests as well. Keep
fixtures, tools, model/effort, permission scope, acceptance criteria, and available
context comparable. Vary one policy or routing choice at a time. Repeat cases and
vary run order before generalizing. Use a fixed total token allowance when the
host can observe it; otherwise report usage and its limitations rather than
claiming an equal-budget experiment.

Keep evaluators and behavior assertions outside candidate write sets. Grade
correctness, missed defects, scope violations, completion, and required gates
before comparing elapsed time, total parent/child/rework tokens, correction rounds,
and human intervention. Count overlapping cumulative usage only once. Record
missing usage as unknown, never zero. A budget-limited unfinished run is incomplete.

Use the parent-only arm only for fixtures whose gates allow self-review; mark it
ineligible when independent review is required. Compare the two reviewed arms
there instead of weakening a real gate. Parent summaries and role names alone
are not dispatch, sandbox, or successful-check evidence.

Record case and fixture revision, raw request, skill revision, comparison arm,
requested/observed models, environment, dispatch trace references, grader result,
side effects, elapsed time, usage coverage, interventions, and remaining work.
Publish a sanitized result record, including failures. A bounded smoke can reveal
a regression; it cannot establish a general quality or cost advantage.

## Compare model and effort selections

After testing topology, hold parent/reviewer settings, review requirements, tools,
fixtures, concurrency and speed mode fixed. Compare eligible implementation
selections from the bundled profile: `routine`, `bounded`, role default, and
`complex`. Include the prior implementation baseline through an explicit
`--model gpt-6-astra --effort high` override; do not create a second default profile.
Do not combine that override with a preset. Resolve every selection against the
current host before starting; unavailable arms remain unexecuted.

Use the two same-model preset pairs to isolate effort changes, and compare
same-effort selections to isolate model changes where possible. Test frozen local
fixes, cross-module implementations, unresolved-root-cause requests and consequential
review cases separately. An ambiguous task tests return-to-parent behavior, not
permission to force every selection to implement it. Use unhinted task requests
for classification tests; keep expected preset names with the evaluator.

Preserve explicit/custom-profile cases, including profiles without presets and
unavailable requested efforts. Grade completion, regressions, scope and review
before efficiency. Record parent supervision and correction work as well as child
usage. Distinguish actual Codex credits, API charges and token estimates; do not
derive subscription savings from public benchmark prices or per-token ratios.
Repeat representative matched cases before claiming an optimal default.

## Explicit-delegation smoke: prepare a bounded case

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
