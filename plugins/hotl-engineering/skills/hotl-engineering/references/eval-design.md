# Eval Design Guide (Generalized)

Procedure for designing an evaluation gate for agent, retrieval, and generation systems. Use
assets/evals/ (run_evals.py, thresholds.json, judge_rubric.md) as the template for the concrete
implementation.

## Three-layer structure (separating cost from signal)

1. **L1 deterministic checks**: Retrieval metrics (recall@k, MRR), regex for prohibited output, format
   validation, refusal detection. Run every time, on every case, at near-zero cost. Do not run L2 on
   cases that already failed L1
2. **L2 LLM-as-judge**: Rubric scoring (three axes — accuracy, faithfulness, completeness — each scored
   1-5). Use temperature 0 plus the median of 3 votes to suppress variance. Run the smoke subset on
   PRs and the full set nightly
3. **L3 human calibration**: Each month, stratified-sample 30 cases (weighted toward failures) and have
   a human score them with the same rubric. If the ±1-point agreement rate falls below 85%, revise the
   judge prompt. Keep the calibration record as an audit trail

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
- Quality score: a **dual threshold** of relative (baseline minus tolerance) and absolute (floor)
  (Principle 8)
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
