# Eval Design Guide (Generalized)

Procedure for designing an evaluation gate for agent, retrieval, and generation systems. Use
assets/evals/ (run_evals.py, thresholds.json, judge_rubric.md) as the template for the concrete
implementation.

Treat sample counts, vote counts, agreement thresholds, and reading-time targets
below as initial design examples. Calibrate them to representative task outcomes,
latency/cost, and human judgments. Judge results are not deterministic (current anthropic
SDKs cannot send sampling parameters such as temperature). Schema validation alone is not a
skill-behavior eval.

## Three-layer structure (separating cost from signal)

1. **L1 deterministic checks**: Retrieval metrics (recall@k, MRR), regex for prohibited output, format
   validation, refusal detection. Run every time, on every case, at near-zero cost. Do not run L2 on
   cases that already failed L1
2. **L2 LLM-as-judge**: Rubric scoring (three axes — accuracy, faithfulness, completeness — each scored
   1-5). Anchor every level with a verifiable description (assets/evals/judge_rubric.md). Keep the
   graded levels because how far a case fell is diagnostic and sets the order of fixes, but never
   gate on the graded score itself. The gate binarizes each axis at the pass line
   (`judge.pass_score` in thresholds.json, default 4) and judges the pass rate per axis. Never sum
   the axes (a sum hides which axis dropped and is hard to calibrate). Do not send sampling
   parameters (anthropic SDK 1.0 and later reject them). Handle variance with the median of 3
   votes and L3 human calibration. Pin the SDK major, and before raising it,
   confirm the arguments and API version with a network-free contract test. Run the smoke subset on
   PRs and the full set nightly
3. **L3 human calibration**: Each month, stratified-sample 30 cases (weighted toward failures) and have
   a human score them with the same rubric, independently of the judge. Binarize both the human and
   the judge scores at the pass line and compute agreement per axis (TPR/TNR). If agreement on clear
   cases falls well below roughly 90%, fix the judge prompt or the rubric (early on, the sample is
   small and the interval wide, so accumulate months before reading it). Keep the calibration record
   (date, judge model ID, rubric version, case IDs, human and judge verdicts, agreement) in the
   adopting repository's evals/calibration/ as an audit trail

## Golden-set category design (this is the core of the design)

Categories to always include:
- **standard / hard**: Ordinary cases and hard cases (notational variants, multi-source integration)
- **no-answer**: Cases where no correct answer exists. Can the system say "not found"?
  (hallucination detection)
- **boundary cases (must-pass)**: Permission boundaries, confidential-information leakage, prompt
  injection. For each domain, identify and design around the boundary where "a single leak is fatal"
  (Principle 9)
- **freshness**: Does it return the updated version of data that has changed?
- **format**: Compliance with the instructed format

Start at 50 cases and grow to 100-150. This only works paired with the operating rule that
**production failure reports become golden-set entries within 24 hours** (Principle 11).

## Gate condition design

- must-pass category: 100%. Block on a single failure. Do not mix it into the average
- Quality score: apply a **dual threshold** of relative (baseline minus tolerance) and absolute
  (floor) to the judge's pass rate per axis (Principle 8). Compare only with a baseline scored at the
  same pass line
- Completeness: block on target/judge execution failures, invalid or missing
  votes, empty selected suites, and mismatched deployed revisions. Keep these
  failures separate from quality averages
- The baseline is the result from "the last main that passed the full suite entirely." Update it
  automatically nightly
- Give smoke (on PRs) a wider tolerance than full (to avoid false blocks from noise)

## Implementation notes

- Isolate the call to the target system in a single function (call_target) to absorb differences in
  the API contract
- **Permission tests must hit the server-side boundary** (a test that passes a permission list from
  the client is meaningless)
- Keep injection-test trap documents permanently in the staging index
- Do not put a golden set containing real data in the repository; fetch it from access-controlled
  storage at CI run time. Keep only sanitized sample data in the repository
- Require the report to be "readable by a human in 3 minutes" (a table of failure cases plus the
  baseline diff). This becomes the evidence for CP4 (promotion approval)
- Changes to the judge model and changes to the rubric itself are also subject to the eval-gate
  (control over meta-changes)
- For workflow skills, test routing and observable tool/artifact behavior in
  isolated fixtures. Include negative trigger cases and forbidden side effects;
  give graders the rubric separately from the task prompt. Record model/runtime,
  skill/input versions, selected cases, tool traces, latency/cost, and the outcome
- Evaluate the same cases before/after a change, repeat representative cases,
  and preserve regressions as fixtures. Never promote from plausible final prose
  when required artifacts or actions are absent
