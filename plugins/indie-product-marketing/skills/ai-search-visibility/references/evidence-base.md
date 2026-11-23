# Evidence Base and Claim Audit

## Contents

1. [How to use this reference](#how-to-use-this-reference)
2. [Evidence grades](#evidence-grades)
3. [State of the evidence](#state-of-the-evidence)
4. [Claim audit](#claim-audit)
5. [Auditing a vendor proposal or case study](#auditing-a-vendor-proposal-or-case-study)
6. [What remains uncertain](#what-remains-uncertain)
7. [Sources](#sources)

## How to use this reference

Use this file to check a claim about AI-answer visibility before it enters a plan, a report, or a purchasing decision. Preserve the distinction between:

- A result that a vendor or founder reports about one product.
- Independent evidence that a mechanism exists.
- Evidence that the mechanism transfers to another product, market, or engine.
- A recommendation that still needs a local test.

Figures in the audit table were checked against the cited source on 2026-11-23 unless a row says *reported*, which means the figure reached this file through secondary coverage and was not re-checked. Re-fetch a source before quoting a number from it.

## Evidence grades

| Grade | Meaning | Appropriate use |
|---|---|---|
| A | Operator documentation, law, first-party raw analytics, or a controlled experiment | Establish a rule or support a mechanism |
| B | Peer-reviewed or transparent observational research with a disclosed sample | Support a likely pattern with limitations |
| C | Vendor or founder study with useful denominators but a commercial interest or no independent check | Generate hypotheses and analogies |
| D | Anecdote, heuristic, unexplained benchmark, or unsupported assertion | Test only; do not present as fact |

## State of the evidence

- **The only causal evidence is experimental, and the experiments run on simulated or API pipelines.** They inject documents into a model's context and observe what gets cited. They do not show what a live product retrieves, and they do not measure traffic.
- **Studies of live engines are almost all observational**, and almost all are published by companies that sell AI-visibility tools or services. A correlation with citations is frequently a marker of an established brand, which has more of everything. The one field intervention reviewed, in which Ahrefs published 34 pages and tracked live answers, had no control group. No study shows a stable causal effect across engines.
- **Operators publish eligibility rules, not ranking factors.** See [engine-eligibility.md](engine-eligibility.md).
- **The system under study keeps changing.** The mix of cited sources has shifted within weeks more than once, and published correlations describe one period.

Read every row below with these four limits in mind.

## Claim audit

| Claim | Verdict | Evidence and correction |
|---|---|---|
| Run search and AI-answer work as one plan | Supported | Google states that eligibility for its AI features is the same as for Search and that optimizing for generative AI search is "still SEO"; Microsoft states that Bing and Copilot share one crawling, indexing, and ranking foundation (A). C-SEO Bench found that improving a source's position in the model's context beat rewriting the document (A, simulated). Overlap between AI Overview citations and the top results is partial, so rank alone is not the whole answer: in early 2026 Ahrefs found 37.9% of cited URLs among the first ten result blocks, and 37.1% counting organic links only. Its earlier study reported about 76%, with a different citation parser, so the two are not a like-for-like trend (C). |
| Rewriting pages with statistics, quotations, and citations lifts visibility by 30–40% | Contradicted outside the original experiment | The figure comes from the GEO paper, which used a simulated engine and measured a relative gain in position-adjusted word count. C-SEO Bench tested the same family of methods across domains and found them "largely ineffective" and frequently negative, with gains shrinking as more competitors adopt them. A 2026 survey of 45 studies concludes that the original gains hold only for a source already placed in a fixed context (A/B). |
| FAQ blocks, summary boxes, page speed, and author bios raise citations | Unverified; the largest observational study points against it | An agency's own study of two million citations reports that these associations reverse or fall to zero once domain is controlled, and that none reaches a conventionally small effect size (C). The study is observational and does not rule out an effect. Google says chunking and writing for AI are unnecessary; Microsoft recommends headings, tables, and FAQ sections (A). Use structure because it helps readers; do not sell it as a citation lever. |
| Schema markup raises citations | Unverified | The same study could extract schema reliably only on third-party pages and found no independent effect there (C). Google says no special schema is needed and that structured data must match the visible text; Microsoft says structured data may support grounding without guaranteeing visibility (A). |
| Fixed formats work: 200–400-word blocks, 40–60-word answers, a 120-word opening | Unverified | No source gives evidence for the numbers. Leading with the answer is reasonable editing practice (D). |
| Add `llms.txt` to be cited | Contradicted for Google; unverified elsewhere | Google Search ignores the file (A). SE Ranking found no relationship between the file and citations across roughly 300,000 domains (C). No other operator states a position. |
| Match pages to the questions buyers actually ask | Conditionally supported, direction only | A controlled study across six models found topical relevance and position in the context to be the largest drivers of being cited first; formatting-only edits had little effect (A, simulated). The agency study above reports the same direction. Its headline measure is word overlap between a page and every prompt in the client's workspace, including prompts that did not cite the page, which avoids the most direct circularity. The prompts were still written by the agency's analysts, and its title and paragraph similarity measures use citing prompts only, which the authors call upper bounds (C). Read the finding as "answer the buyer's question directly," not as "mirror prompt wording." |
| Explicit prices and recent dates help | Plausible | The same controlled study found that explicit price information and a recent timestamp helped consistently (A, simulated). The agency study reports that pricing pages are cited more than other formats (C). Changing only a date is not an update. |
| Third-party mentions drive AI visibility | Conditionally supported as a correlation | Across 75,000 brands, Ahrefs found brand web mentions correlated with AI Overview visibility at 0.664 against 0.218 for backlinks, and says the factors may only mark existing brand strength (C). An academic comparison reports a strong bias in AI search toward third-party sources over brand-owned pages, and a bias toward large brands (B). No study isolates cause. Google says seeking inauthentic mentions "isn't as helpful as it might seem" (A). |
| Target one platform, such as Reddit, because AI engines cite it most | Conditionally supported and unstable | Citation shares differ by engine and move sharply. Semrush observed Reddit in close to 60% of ChatGPT responses in early August 2025 and about 10% by mid-September (C). Moderators and the platform itself have acted against seeded posts (*reported*). Measure which sources the product's own prompts cite before choosing where to work. |
| Publish or get listed in "best X" pages to be recommended | Conditionally supported, with a gap between citation and recommendation | "Best X" lists were 43.8% of the page types ChatGPT cited across 750 top-of-funnel recommendation prompts for software, products, and agencies in an Ahrefs sample; the figure does not describe implementation or support questions (C). In AI Overviews, a self-promotional list that was cited left its own brand out of the recommendation 69% of the time (C). In an Ahrefs experiment, 43% of answers citing a page that promoted a little-known brand never named it, against 11% for a well-known product, and about a quarter of citations appeared once and never returned (C). |
| A single check of a prompt shows whether the product is visible | Contradicted | SparkToro found less than a 1-in-100 chance of receiving the same brand list twice (C). The IAB guideline states that single-response measurement is not measurement (B). See [measurement.md](measurement.md). |
| A tracker's number is what users see | Unverified | For brands with at least 20% visibility, Graphite measured a mean pairwise cosine similarity of 0.48 between the brand sets returned by the API and by logged-out product sessions, against 0.70 and 0.76 within each (C). Signed-in sessions were not measured. Google states that no third-party tool has access to its internal ranking or AI systems (A). Ask which surface a number came from. |
| A mention rate that mixes in prompts naming the brand shows how often buyers discover the product | Contradicted | Prompts that contain the brand name pull the brand into the answer. One agency audit reports a client set at 10.8% overall and 1.9% on prompts without the brand (C, single example). A mixed rate is a valid number only when it is labeled as mixed; report branded and unbranded prompts separately. |
| Visitors from AI assistants convert better | Unverified; varies by period and vertical | A study of 973 e-commerce sites found ChatGPT referrals converting below every established channel except paid social in 2024–25 (B). Vendor reports claim the opposite for other periods (*reported*). None measures product activation. |
| A large relative gain proves the program worked | Unverified without the inputs | A ratio such as +500% citation rate or 40 times more AI-attributed users means little without baseline counts, metric definitions, the prompt set, the engines, the attribution method, and what else changed in the period. Starting from near zero makes any ratio large. |
| Results arrive within days or weeks | Unverified | Citations appear and disappear quickly, so an early appearance is not a stable position. Decide the observation window before starting. |
| Click analytics show the size of the AI channel | Incomplete | In one agency's lead records, 189 leads named an AI assistant as their source and first-touch attribution credited 28 of them (C). Google reports AI feature traffic inside ordinary web search data (A). |
| Undisclosed community posts, paid links, and assistant-memory instructions are effective shortcuts | High policy risk | These collide with platform rules, search spam policies, and advertising-disclosure law regardless of effect. See [off-site-rules.md](off-site-rules.md). |

## Auditing a vendor proposal or case study

Ask for the following before treating a reported result as evidence. A proposal that cannot answer them may still be honest, but it is a reported fact, not an observed one.

**The numbers**

- Baseline and endpoint as counts, not only as a ratio.
- The definition of each metric, and whether prompts that name the brand were excluded.
- The prompt set: how many prompts, how they were chosen, how many runs each, which engines, which surface (API or product), which dates.
- Whether the baseline was reset during the engagement, and when.
- Who measured it. A vendor's own tool measuring the vendor's own work is not independent.

**The business outcome**

- How visitors or signups were attributed to AI assistants.
- What else changed in the period: launches, funding, press, pricing, seasonality, model or product releases by the engines.
- Whether a comparison group or an unaffected segment exists.

**The methods**

- Which accounts post in communities, who operates them, and how the relationship is disclosed in each post.
- Whether any placement, link, or review involves payment, exchange, or an incentive, and how it is labeled.
- What the vendor promises. No operator guarantees placement, so nobody else can.

**The fit**

- The domain strength, brand awareness, budget, and team size of the case compared with the product in question. In the agency study above a domain-level term explains more of the variation than the page features do, although the authors caution that this does not rank causal levers. Either way, a result from an established brand is not a forecast for a new site.

The agency case study that prompted this skill is a useful exercise. It reports a 4,600% increase in monthly activated users attributed to AI since January 2026 and a 558% increase in unbranded citation rate from January to August 2026, the latter measured with the agency's own tracker, for a funded company that started at a Domain Rating of 70. It does not state baseline counts, metric definitions, prompt numbers, engines, or the attribution method, and it notes that the baseline was reset when scope changed. Its planning method is reusable; its ratios are not a forecast. Two of the frameworks it names, CITABLE for page structure and Own / Claim / Earn / Contest for third-party sources, are the agency's own.

## What remains uncertain

- How much personalization, memory, account state, and location change what a real user sees. No controlled study was found.
- Whether findings from English-language B2B software and e-commerce transfer to other languages, markets, and consumer products. Which sources an engine cites for Japanese-language questions was not studied in the sources reviewed.
- The share of AI-influenced visits that arrive without a referrer. Published figures come from single vendors with different definitions.
- How long any observed advantage lasts after an engine changes its retrieval pipeline.
- The accuracy of commercial AI-visibility trackers. No independent audit was found.

## Sources

Retrieved 2026-11-23.

**Experiments**

- Aggarwal et al., [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735), KDD 2024.
- Puerto et al., [C-SEO Bench](https://arxiv.org/abs/2506.11097), NeurIPS Datasets and Benchmarks 2025.
- Vishwakarma et al., [What Gets Cited](https://arxiv.org/abs/2605.25517), preprint, 2026-05-25.
- Martinez, [critical survey of 45 GEO studies](https://arxiv.org/abs/2607.14035), preprint, 2026-07-15.

**Observational research**

- Chen et al., [comparison of AI search and web search sourcing](https://arxiv.org/abs/2509.08919), preprint, 2025-09-10.
- Kaiser and Schulze, ChatGPT referrals to e-commerce websites, Marketing Science, 2026; summarized by [Frankfurt School](https://www.frankfurt-school.de/home/news/2026/06/chatgpt-in-online-ohopping).
- Ahrefs (sells an AI-visibility product): [brand mention correlations](https://ahrefs.com/blog/ai-overview-brand-correlation/), [AI Overview citations and the top 10](https://ahrefs.com/blog/ai-overview-citations-top-10/), ["best X" lists](https://ahrefs.com/blog/best-lists-research/), [self-promotional content experiment](https://ahrefs.com/blog/self-promotional-content-ai-seo-experiment/).
- Lily Ray, [self-promotional lists in AI Overviews](https://lilyraynyc.substack.com/p/why-calling-yourself-the-best-could), 2026-06-17.
- Semrush (sells an AI-visibility product): [most-cited domains](https://www.semrush.com/blog/most-cited-domains-ai/), 2025-11-10.
- SE Ranking (sells an AI-visibility product): [llms.txt study](https://seranking.com/blog/llms-txt/).
- Discovered Labs (sells answer-engine optimization services): [What actually drives AI citations](https://discoveredlabs.com/research/what-drives-ai-citations) and its preprint [arXiv:2609.35077](https://arxiv.org/abs/2609.35077); [measurement test bed](https://discoveredlabs.com/blog/aeo-test-bed-noise-vs-signal); [Granola case study](https://discoveredlabs.com/case-studies/granola); [CITABLE framework](https://discoveredlabs.com/blog/citable-the-aeo-content-framework-we-use-to-get-b2b-brands-cited-by-ai).

**Measurement**

- IAB, [Measuring Visibility in the AI Era](https://www.iab.com/wp-content/uploads/2026/07/IAB_Measuring_Visibility_in_the_AI_Era_August_2026-1.pdf), August 2026.
- Graphite (an agency): [Demystifying randomness in AI](https://graphite.io/five-percent/demystifying-randomness-in-ai), 2026-04-14.
- SparkToro with Gumshoe (sells AI tracking): [AI recommendation consistency](https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/), 2026-01-28.
- Omniscient Digital (an agency): [first-touch versus self-reported attribution](https://beomniscient.com/blog/first-touch-vs-self-reported-attribution-aeo/), 2026-08-28.
