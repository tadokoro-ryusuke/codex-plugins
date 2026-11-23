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

Give prompt variants of one buyer question the same question ID, so the question counts once. A prompt ID stands for one fixed wording; give a reworded prompt a new ID. Remove names, company identifiers, and confidential details from prompts taken from customer conversations. Report branded and unbranded prompts separately. State the number of unbranded questions beside every rate; fewer than 50 is exploratory.

## Run protocol

- Engines:
- Surface (consumer product or API) and why:
- Runs per prompt:
- Session state (new conversation, memory and custom instructions off, signed in or out):
- Locale and device:
- Who runs the prompts and how (by hand, official API), and the authorized API spend:
- What counts as an answer on each surface:
- Same-day repeat snapshots (labels, dates, and the differences the script reported):

Record one line per run, including runs that failed or showed no AI answer:

```json
{"snapshot": "2026-11-baseline", "engine": "chatgpt", "surface": "product", "prompt_id": "P-01", "run_id": "2026-11-baseline/chatgpt/P-01/01", "branded": false, "mentioned": false, "cited": false}
{"snapshot": "2026-11-baseline", "engine": "chatgpt", "surface": "product", "prompt_id": "P-02a", "question_id": "Q-02", "run_id": "2026-11-baseline/chatgpt/P-02a/01", "branded": false, "mentioned": true, "cited": false}
{"snapshot": "2026-11-baseline", "engine": "chatgpt", "surface": "product", "prompt_id": "P-02b", "question_id": "Q-02", "run_id": "2026-11-baseline/chatgpt/P-02b/01", "branded": false, "status": "no_answer"}
```

A prompt with no `question_id` is its own question. When a question has several prompt variants, put the same `question_id` on every one of them, including the original. `status` is `answered` when omitted, or `no_answer` or `error`; leave `mentioned` and `cited` out for those. Keep the detail for each answered run beside its run ID:

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
- The one comparison the decision rests on (engine, surface, prompt type, metric):
- Largest difference seen between same-day repeats:
- Continue if:
- Revise if:
- Stop if:
- Business outcome checked alongside (metric, source, definition):

## Results

Paste the script output for each snapshot and comparison.

### Summary

### Comparison with the previous snapshot

### Reading

- Changes judged real (clearly larger than the same-day differences, and persisting in a further snapshot):
- Inconclusive changes:
- Counts and first appearances where the baseline is zero or near zero:
- Questions left out of the comparison, and why:
- Runs with no AI answer, and failed runs:
- Runs that cited the product's page without naming the product:
- Inaccurate descriptions of the product found:
- Sources cited most often (carry to the source ledger):
- Engine-side changes suspected:
- Decision under the predeclared rule:
