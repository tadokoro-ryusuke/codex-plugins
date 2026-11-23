# Measurement

## Contents

1. [Three layers](#three-layers)
2. [Metric definitions](#metric-definitions)
3. [Build the prompt set](#build-the-prompt-set)
4. [Run a snapshot](#run-a-snapshot)
5. [Summarize and compare](#summarize-and-compare)
6. [Read the result](#read-the-result)
7. [Traffic and business outcomes](#traffic-and-business-outcomes)
8. [Blind spots](#blind-spots)
9. [Sources](#sources)

## Three layers

Keep three kinds of evidence apart in every report:

1. **Eligibility** — whether the engines can crawl, index, and show the pages. Checked once and after changes; see [engine-eligibility.md](engine-eligibility.md).
2. **Presence** — how often answers to a fixed set of prompts mention the product or cite its pages. A rate with an interval, per engine and surface.
3. **Outcome** — visits, signups, and activated users that can be tied to AI assistants.

Presence is not demand. A product can be cited often and gain no users, and a product can gain users from answers that never link to it. Never present a presence metric as a business result.

## Metric definitions

The IAB guideline *Measuring Visibility in the AI Era* (August 2026) defines the core metrics:

| Metric | Definition |
|---|---|
| Mention rate | Responses containing a mention of the brand, divided by total responses. |
| Citation rate | Responses in which the brand's content or domain is cited as a source, divided by total responses. |
| Share of voice | The brand's mentions as a proportion of all brand mentions within a defined competitive category. |

Tools and operators use other definitions under the same names. Some weight share of voice by position in the answer. OpenAI's Business Hub counts a mention for an online business only when ChatGPT references the business's website. Write the definition beside every number and never compare rates that were defined differently.

This skill uses these working definitions:

- **Mentioned** — the answer text names the product or the company.
- **Cited** — the answer links to, or names as a source, a page on the product's own domain.
- **Third-party citation** — the answer cites another site's page that mentions the product. Record the URL; do not count it as a citation.
- **Unbranded prompt** — a prompt that contains neither the product name, the company name, nor the domain. No standard defines this term, so state it.
- **Answered run** — a run in which the engine produced an AI answer. A search that showed no AI answer, and a failed request, are recorded with their own status and stay out of the rates.

The bundled script reports two numbers under each rate. The headline is the **mean of per-question rates**, which gives every buyer question the same weight. Beside it are the pooled hits and runs, which correspond to the IAB definition. They differ when questions have different numbers of runs; label whichever one is quoted.

## Build the prompt set

The prompt set is a sample of the questions buyers ask. Its quality limits everything measured with it; the IAB guideline notes that rates are sensitive to query set composition.

**Draw prompts from buyer behavior, not from imagination.** Use search-console queries, support questions, sales and onboarding conversations, community threads, reviews of substitutes, and the comparisons buyers already search for. Record where each prompt came from. A set hand-picked by the person hoping for a good number is a biased sample.

**Remove personal and confidential detail first.** A prompt sent to an engine leaves the user's control. Keep the buying intent and the constraints; strip names, company identifiers, account details, and anything a customer shared in confidence. Use only data the user has agreed to use for measurement.

**Cover the decisions, not the keywords.** Include problem-aware questions, category questions, comparisons and alternatives, implementation questions, and switching questions. Write each prompt the way a buyer would, with the situation and constraints that shape the answer: team size, budget, platform, existing tools, location, deadline.

**Use one prompt per buyer question, or group the variants.** Ten rewordings of one question are not ten independent questions. Either keep a single prompt for each question or give the variants the same `question_id`, so the question counts once.

**Prefer breadth of intent to precise wording.** In a study of human-written prompts for one purchase, the prompts were almost unrelated in wording while the brands recommended stayed broadly similar. Chasing an exact phrasing adds little.

**Tag every prompt branded or unbranded.** A prompt that names the product pulls the product into the answer. Keep branded prompts to check accuracy and sentiment, and report them in a separate row. One agency audit found a prompt set that reported 10.8% overall and 1.9% once branded prompts were removed.

**Size the set honestly.** The IAB guideline treats fewer than 50 queries per measurement program as exploratory. A solo product can start with 20 to 30 unbranded questions when the report says so. Halving the interval takes roughly four times as many questions.

**Write prompts in the buyer's language and note the locale.** Results for one language or country do not describe another.

**Freeze and version the set.** Adding or rewording prompts starts a new series. Compare two snapshots only on the questions they share.

Copy `../assets/prompt-set.md` into the user's project to record the set. Do not write a product's data into the skill's own files.

## Run a snapshot

A snapshot is one pass over the whole prompt set on each engine within a short window.

- **Choose the engines buyers use**, and keep each engine's results separate. Engines cite different sources and move independently.
- **Repeat every prompt.** One response is a sample of one. In Graphite's test, the mean absolute error across the brands in a prompt's answers was 5.6 points at 10 responses per prompt, and 9.1 points for brands with at least 10% visibility; at 40 responses, 94.9% of prompts had a mean absolute error within 5 points. Those figures describe its panel, not the precision of one product's rate or of a before-and-after difference. Start with about 10 runs per prompt, then set the number from the interval the script reports for the metric the decision depends on.
- **Start each run clean.** Use a new conversation with memory, custom instructions, and prior context off, and note whether the session was signed in.
- **Fix the surface.** Answers from an API and from the consumer product differ. For brands with at least 20% visibility, Graphite measured a mean pairwise cosine similarity of 0.48 between the brand sets from the API and from logged-out product sessions, against 0.70 and 0.76 within each. Prefer the surface buyers use, record it on every run, and never mix surfaces in one series.
- **Respect the engine's terms and the user's budget.** Run prompts by hand or through an official API. Check the terms before automating a consumer interface, and spend API credit only as the user has authorized.
- **Record every run, including the ones without an answer.** Give each run a unique ID and note the snapshot label, date, engine, surface, model or mode if shown, locale, prompt ID, branded flag, and status: answered, no AI answer shown, or failed. For an answered run, record whether the product was mentioned, whether its own page was cited, the URLs cited, the competitors named, and whether the description of the product was accurate. Decide before the snapshot what counts as an answer on each surface.
- **Measure same-day variability once.** Before the first comparison, run the set twice on the same day and compare the two. The IAB guideline treats a movement as meaningful only when it exceeds what re-running the same queries on the same day would produce.

## Summarize and compare

`../scripts/visibility-stats.mjs` turns run records into rates with intervals. It needs Node.js and no dependencies.

Input is a JSON array or JSON Lines, one object per run:

```json
{"snapshot": "2026-11-baseline", "engine": "chatgpt", "surface": "product", "prompt_id": "P-07", "run_id": "2026-11-baseline/chatgpt/P-07/03", "branded": false, "mentioned": true, "cited": false}
```

Optional fields: `question_id` groups prompt variants of one buyer question and defaults to `prompt_id`; `status` is `answered` by default, `no_answer` when the engine showed no AI answer, and `error` for a failed run. `mentioned` and `cited` are required only for answered runs.

```bash
node scripts/visibility-stats.mjs summarize runs.jsonl
node scripts/visibility-stats.mjs compare runs.jsonl --from 2026-11-baseline --to 2027-01-check
```

Add `--json` for machine-readable output.

What it does:

- **Rejects ambiguous input.** A missing `branded` flag, a repeated `run_id`, a prompt that is branded in one row and unbranded in another, or a prompt assigned to two questions stops the run with the row number.
- **Keeps series apart.** Each snapshot, engine, surface, and prompt type is its own row. A comparison pairs only the same engine, surface, and prompt type, and reports any group present in just one snapshot as not comparable.
- **Uses the buyer question as the unit.** Each question's rate over its answered runs counts once. Runs with no AI answer and failed runs are counted and reported, and stay out of the rates.
- **Reports an approximate 95% interval from the spread between questions.** The spread reflects both the choice of questions and run-to-run noise; repeating runs narrows only the second part.
- **Compares two snapshots through the difference on each shared question,** and lists the questions present in only one of them.
- **Counts answered runs that cite the product's page without naming the product.**

Read the interval with its assumption in view. It describes buyers' questions in general only if the questions are an independent, representative sample of what buyers ask. For a hand-picked or narrow set, it describes that set, and the right wording is "on this prompt set."

Three cases produce something other than that interval:

- **One question, or every question with the same fractional rate:** no interval. Add questions or runs.
- **Every question at zero, or every question at one:** a spread-based interval would have zero width and read as certainty. The script reports a bound computed from the number of questions, whatever the number of runs. Report counts.
- **Every question moved by the same amount between snapshots:** no interval and no directional verdict.

The method follows Miller, *Adding Error Bars to Evals*: standard errors of the mean over questions, related questions treated as one cluster, repeated sampling to reduce within-question variance, and paired differences when the same questions are measured twice.

## Read the result

- **Report the rate, the interval, the number of questions, and the hits and runs together.** A rate alone hides how little data stands behind it.
- **Near zero, report counts.** A new product usually has an unbranded mention rate of zero. Percentage change from zero is undefined and from near zero is meaningless. Report hits, the number of questions with at least one hit, and first appearances.
- **Treat a change as real only when three things hold:** the paired interval excludes zero, the difference is larger than the same-day variability measured earlier, and another snapshot agrees. The script reports only the first. When the interval includes zero the result is inconclusive, which is not evidence that nothing changed.
- **Consider the engine before crediting the work.** When competitors move together on one engine, an engine-side change is a likely cause. Look for corroboration, such as a release note or the same shift on unrelated prompts, before starting a new baseline. Start one after a known model or product release, a prompt-set change, or a surface change, and report the two series separately.
- **Separate being cited from being named.** A page can be cited as a source while the answer recommends someone else. The script counts those runs; read them.
- **Record inaccuracies.** An answer that names the product with a wrong price, feature, or status is a finding for the source ledger, not a success.

## Traffic and business outcomes

**Operator reports.** Use what the operators provide before a third-party tool, and record an unavailable report as unavailable, not as zero:

- Google Search Console: the generative AI performance report (impressions in AI features). It does not appear until a site has enough impressions in those features. AI feature traffic is also included in the ordinary Performance report under the Web search type.
- Bing Webmaster Tools: the AI Performance report (citation counts and sampled grounding queries).
- OpenAI Business Hub: aggregate mentions and website clicks over 28 days, after claiming and verifying the business. OpenAI says a blank metric can mean activity below the reporting threshold, data still being collected, or no reporting, and does not necessarily mean zero.

**Analytics.** Build a channel rule for assistant referrers, and expect it to undercount. A third-party compilation from April 2026 describes the following behavior. Operators do not document it, and it changes, so confirm each row in the product's own analytics before relying on it.

| Path | How it tends to appear |
|---|---|
| ChatGPT in a browser | Referrer `chatgpt.com`; links may carry `utm_source=chatgpt.com` with no medium, which some analytics tools leave unassigned |
| ChatGPT mobile apps, and the Atlas desktop app on macOS | No referrer; counted as direct |
| Claude in a browser | Referrer `claude.ai`, passed inconsistently |
| Claude apps | No referrer; counted as direct |
| Google AI Overviews and AI Mode | Indistinguishable from ordinary Google organic search |

**Self-reported source.** Ask "How did you hear about us?" as free text at signup or purchase, and compare it with click attribution. In one agency's lead records, 189 leads named an AI assistant and first-touch attribution credited 28 of them; most of the rest were filed as organic search or direct. Self-report measures recall and only among people who answer, so treat it as a cross-check.

**Outcome metric.** Judge the channel by activated and retained users in the source cohort, with the definitions from the product's growth scorecard, not by sessions or citations. When reporting AI-attributed users, state how attribution was done, the window, and what else changed in the period.

## Blind spots

The sources reviewed for this reference contained no answer to the following:

- The share of clicks from apps and in-app browsers that lose the referrer.
- How many buyers see the product in an answer and arrive later through a branded search or a direct visit.
- The effect of memory, account history, and location on what an individual sees.
- How well synthetic prompts represent real ones. The studies reviewed used prompts written for the study, not logs of real conversations.
- The accuracy of commercial trackers. No independent audit was found.

State these limits in any report that includes an AI-channel number.

## Sources

Retrieved 2026-11-23.

- IAB, [Measuring Visibility in the AI Era](https://www.iab.com/wp-content/uploads/2026/07/IAB_Measuring_Visibility_in_the_AI_Era_August_2026-1.pdf), August 2026.
- Miller, [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640), 2024.
- Graphite (an agency), [Demystifying randomness in AI](https://graphite.io/five-percent/demystifying-randomness-in-ai).
- SparkToro with Gumshoe (sells AI tracking), [AI recommendation consistency](https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/).
- Discovered Labs (sells answer-engine optimization services), [measurement test bed](https://discoveredlabs.com/blog/aeo-test-bed-noise-vs-signal).
- Omniscient Digital (an agency), [first-touch versus self-reported attribution](https://beomniscient.com/blog/first-touch-vs-self-reported-attribution-aeo/).
- SearchPilot (sells SEO testing), [AI platform click referrer reference](https://www.searchpilot.com/hubfs/pdfs/ai-traffic-source-reference.pdf), April 2026.
- Google, [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) and [Generative AI performance report](https://support.google.com/webmasters/answer/16984139); Microsoft, [AI Performance in Bing Webmaster Tools](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview); OpenAI, [Setting up your business on ChatGPT](https://help.openai.com/en/articles/20001635-setting-up-your-business-on-chatgpt).
