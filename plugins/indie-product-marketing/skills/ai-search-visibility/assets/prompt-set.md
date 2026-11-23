# AI Visibility Prompt Set and Snapshot Log

Record the prompt set, how each snapshot was run, and what the numbers showed. Keep the set frozen between snapshots; a changed set starts a new series.

## Set definition

- Set version and date frozen:
- Product and company names that count as a mention:
- Domains that count as a citation:
- Competitors tracked:
- Definition of an unbranded prompt:
- Languages and locales:
- Where the prompts came from:

## Prompts

| Prompt ID | Prompt text | Branded | Intent type | Question ID | Origin | Added in version |
|---|---|---|---|---|---|---|
| P-01 |  | no |  |  |  |  |

Give prompt variants of one buyer question the same question ID, so the question counts once. Remove names, company identifiers, and confidential details from prompts taken from customer conversations. Report branded and unbranded prompts separately. State the number of unbranded questions beside every rate; fewer than 50 is exploratory.

## Run protocol

- Engines:
- Surface (consumer product or API) and why:
- Runs per prompt:
- Session state (new conversation, memory and custom instructions off, signed in or out):
- Locale and device:
- Who runs the prompts and how (by hand, official API), and the authorized API spend:
- What counts as an answer on each surface:
- Same-day repeat run completed on, and the difference observed:

Record one line per run, including runs that failed or showed no AI answer:

```json
{"snapshot": "", "engine": "", "surface": "", "prompt_id": "", "question_id": "", "run_id": "", "branded": false, "status": "answered", "mentioned": false, "cited": false}
```

`status` is `answered`, `no_answer`, or `error`. Keep the detail for each answered run beside its run ID:

| Run ID | URLs cited | Competitors named | Product named without its page cited, or page cited without the product named | Inaccurate statement about the product |
|---|---|---|---|---|
|  |  |  |  |  |

## Snapshot log

| Snapshot label | Dates | Engines | Surface | Model or mode shown | Prompts | Runs per prompt | Changes since the previous snapshot |
|---|---|---|---|---|---:|---:|---|
|  |  |  |  |  |  |  |  |

List engine or model releases, site changes, and off-site work under "changes", so a move can be traced to a candidate cause.

## Predeclared decision rule

Write this before the next snapshot is run.

- Observation window:
- Primary metric and engine:
- Continue if:
- Revise if:
- Stop if:
- Business outcome checked alongside (metric, source, definition):

## Results

Paste the script output for each snapshot and comparison.

### Summary

### Comparison with the previous snapshot

### Reading

- Changes judged real (interval excludes zero, larger than same-day variability, and confirmed by another snapshot):
- Inconclusive changes:
- Counts and first appearances where the baseline is zero or near zero:
- Runs with no AI answer, and failed runs:
- Runs that cited the product's page without naming the product:
- Inaccurate descriptions of the product found:
- Sources cited most often (carry to the source ledger):
- Engine-side changes suspected:
- Decision under the predeclared rule:
