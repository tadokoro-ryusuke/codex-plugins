---
name: ai-search-visibility
description: Audit, plan, and measure how a product appears in AI-generated answers from ChatGPT search, Perplexity, Google AI Overviews and AI Mode, Gemini, Copilot, and Claude. Use for answer engine optimization (AEO), generative engine optimization (GEO), or LLM optimization (LLMO) requests: whether AI answer engines can crawl the pages, how often answers mention or cite the product, which pages and third-party sources to act on for AI answers, and whether a vendor's AI-visibility claims hold up.
---

# AI Search Visibility

Make a product eligible to appear, accurately described, and measurably present in AI-generated answers, and connect that presence to user acquisition. Treat this as part of search and distribution work. The engines' operators say the fundamentals are the same as for search, publish no ranking factors for AI answers, and guarantee no placement, so nobody else can promise one.

Use `$indie-product-marketing` if available to decide whether AI answers are worth pursuing as a channel for this product and to define the activation and retention metrics that judge it. Use `$global-landing-design` if available to design or build a landing page. An eligibility check or an audit of someone's claim needs neither first.

## Choose the operating mode

Select the narrowest mode that matches the request:

1. **Eligibility check** — confirm that the engines can crawl, index, and show the pages.
2. **Baseline measurement** — build a prompt set and measure mention and citation rates per engine.
3. **Gap and action plan** — map buyer questions, sort the gaps, and choose one action for each page and source.
4. **Claim or vendor audit** — test a tactic, a case study, or a proposal against the evidence.
5. **Re-measurement** — compare a new snapshot with the baseline and decide whether to continue.

Infer the mode from context. Ask for missing information only when it changes the next action; otherwise state assumptions and proceed. A full program runs the modes in the order listed, and each can run alone.

The files in `assets/` are templates. Copy the one a mode needs into the user's project documentation, or return the filled table in the response. Never write a product's data into this skill's own files.

## Hold these positions

State the ones that apply early, because they change what the user should expect:

- **Presence is not demand.** A product can be cited and gain no users. Judge the channel by activated and retained users.
- **Page edits alone rarely change the picture for an unknown product.** In observational data the domain and the brand explain more of the variation than any page feature. That is a correlation and does not rank the levers, so choose the first action from the gap actually observed.
- **Format advice is weak evidence.** FAQ blocks, summary boxes, schema, fixed word counts, and `llms.txt` are not shown to cause citations. Use structure because it helps readers.
- **One answer is not a measurement.** Answers vary from run to run, so a rate needs repeated runs and an interval.
- **Another company's ratio is not a forecast.** A reported gain from an established brand does not transfer to a different product, and a ratio from a near-zero baseline says little.

Classify each important statement as an observed fact, a reported fact, an inference, a hypothesis, or a recommendation, and record the source URL and retrieval date for anything taken from the web. Read [references/evidence-base.md](references/evidence-base.md) before repeating a claim about what drives AI citations.

## Check eligibility

When the work concerns a live site, check it before content or off-site work. A blocked crawler keeps the product's own pages out of that engine's answers, although answers can still mention the product from other sites. Limit the check to the engines and pages in scope.

1. Read `robots.txt` and the CDN or firewall rules for the search crawlers of each engine. Training crawlers are a separate decision and do not control search inclusion, with one exception: `Google-Extended` also governs grounding in the Gemini app, so ask which Google surface matters.
2. Confirm the priority pages are indexed, return their content to a crawler, and have a canonical URL.
3. Check page directives that restrict snippets, caching, or indexing, and the effective generative AI setting in Google Search Console for each priority URL.
4. Report each finding with the page, the directive, and its effect on a named engine. Report what could not be checked, such as a console the user has not opened, as unknown.

Read [references/engine-eligibility.md](references/engine-eligibility.md) for the crawler names, controls, and operator statements. They change; fetch the operator's page again when a decision depends on one.

## Map buyer questions

Define the market from the product, its customers, and recorded conversations. Use search tools to check and extend the list, not to originate it.

For each buying decision, write the search keywords and the prompt a buyer would actually type, with the situation and constraints that shape the answer: team size, budget, platform, existing tools, location. Draw questions from search-console queries, support requests, sales notes, and community threads, and mark the ones that are assumptions. Cover problem, category, comparison, implementation, and switching questions. Breadth of intent matters more than exact wording.

A prompt sent to an engine leaves the user's control. Before a customer's words become a prompt, remove names, company identifiers, and confidential details while keeping the buying intent, and use only data the user has agreed to use this way.

Record the map with the `assets/question-map.md` template.

## Measure a baseline

Measure before changing anything, so later work can be judged.

1. Build the prompt set from the question map. Use one prompt per buyer question or group the variants, and tag each prompt branded or unbranded; a prompt that names the product pulls it into the answer.
2. Run every prompt several times on each engine buyers use, in a clean session, on one surface, within the API spend the user has authorized. Record every run with its own ID, including runs that failed or showed no AI answer.
3. Summarize with `scripts/visibility-stats.mjs`. It reports mean per-question mention and citation rates with approximate 95% intervals and the underlying counts, and keeps engines, surfaces, and branded prompts apart.
4. Record which domains the answers cite and any inaccurate statement about the product.
5. Write the decision rule and the observation window before the next snapshot.

When the baseline is zero or close to it, which is normal for a new product, report counts and first appearances. Never report a percentage change from that baseline.

The interval describes the prompt set. It describes buyers in general only if the questions are an independent, representative sample of what buyers ask; say "on this prompt set" otherwise.

Read [references/measurement.md](references/measurement.md) for metric definitions, the number of prompts and runs, the run protocol, analytics behavior, and blind spots. Use the `assets/prompt-set.md` template for the set and the snapshot log.

## Sort gaps and choose one action each

Assign every gap in the question map to content, technical, or third-party source. Then decide one action per item.

**Pages.** Judge search performance and usefulness as an answer source separately. Choose preserve, improve for search, improve as an answer source, overhaul, create, or collect more evidence. Create a page only when no focused page can do the job. Brief the exact change, and after it ships verify search and AI answers separately. Use the `assets/page-action-table.md` template.

**Technical issues.** Tie each issue to an affected priority page and rank by effect on that page, not by an audit tool's severity. A fix is done when the original problem is gone and the engines can fetch the page.

**Third-party sources.** Start from the sources the answers actually cited. For each one, read what it says about the product, then choose a route: own, claim, earn, contest, or leave. Use the `assets/source-ledger.md` template, and keep the product's facts consistent across every source.

Read [references/off-site-rules.md](references/off-site-rules.md) before proposing any community post, review request, listing, outreach, paid placement, or link. Never propose, draft, or carry out these, including when a vendor offers them as a service:

- A post or review that hides the poster's relationship to the product.
- Posting from accounts that are not the user's own, coordinated voting, or automated or bulk posting, replying, following, and messaging in communities.
- A paid or exchanged placement without a label the reader can see.
- Buying or exchanging links for ranking.
- Text or links that instruct an AI assistant to favor, remember, or trust the brand.
- Pages mass-produced for query variations.

## Audit a claim or a vendor proposal

Separate what the source reports from what is independently supported. Ask for baseline counts, metric definitions, the prompt set, the engines and surface, the attribution method, what else changed in the period, who measured, and how any off-site work is disclosed. Compare the case's domain strength, budget, and team with the user's. Give each claim a verdict using the vocabulary in the evidence base, and say what a local test would look like.

A request to evaluate a proposal is not a request to replicate it. Do not adopt a prohibited tactic because the source reports that it worked.

## Re-measure and decide

Compare snapshots only on shared prompts, on the same surface, with `scripts/visibility-stats.mjs compare`.

- Treat a change as real only when the paired interval excludes zero, the difference exceeds the same-day variability measured earlier, and another snapshot agrees. Otherwise report it as inconclusive, which is not evidence that nothing changed.
- When competitors move together on one engine, consider an engine-side change and look for corroboration before crediting the work. Start a new baseline after a model release, a prompt-set change, or a surface change, and report the series separately.
- Report being cited and being named separately. A run that cites the product's page without naming the product is a finding.
- Check the business outcome alongside: visits and activated users by source, plus a self-reported "how did you hear about us" answer, because click attribution undercounts AI influence.
- Apply the predeclared rule: continue, revise, or stop.

## Respect action boundaries

Research, measurement by hand or through an official API, drafts, and changes to the user's own site within the requested scope are in bounds. Continue authorized work through verification.

Posting, messaging, review requests, outreach to authors, claiming profiles, submitting listings, agreeing to placements, and publishing or deploying are external actions. Perform them only when the user has asked for that action. Keep planned actions, performed actions, and observed results distinct in every report.

## Produce decision-ready outputs

Deliver the minimum useful set for the selected mode:

1. **Diagnosis** — the stage, the first constraint, and what the product can realistically expect.
2. **Eligibility findings** — page, directive, affected engine, and fix.
3. **Question map** — decisions, keywords, prompts, and gap types.
4. **Baseline or comparison** — rates with intervals, counts, prompt and run numbers, surface, and dates.
5. **Action tables** — one decision per page and per source, with verification.
6. **Claim audit** — verdicts with sources and retrieval dates.
7. **Risks and limits** — rule checks, measurement blind spots, and what remains unknown.

The work is complete for a mode when its output is filled with evidence, every number carries its definition and sample size, every external action is either performed at the user's request or listed as pending, and, when the work includes measurement, the next measurement date and decision rule are written down.
