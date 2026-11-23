# Engine Eligibility and Operator Statements

## Contents

1. [How to use this reference](#how-to-use-this-reference)
2. [Eligibility checklist](#eligibility-checklist)
3. [Google Search: AI Overviews and AI Mode](#google-search-ai-overviews-and-ai-mode)
4. [OpenAI: ChatGPT search](#openai-chatgpt-search)
5. [Perplexity](#perplexity)
6. [Anthropic: Claude web search](#anthropic-claude-web-search)
7. [Microsoft: Bing and Copilot](#microsoft-bing-and-copilot)
8. [Where operators disagree](#where-operators-disagree)
9. [Claims with no first-party support](#claims-with-no-first-party-support)
10. [Sources](#sources)

## How to use this reference

Use this file to separate what the operators of AI answer engines document from what agencies and tools claim. Only the operators' own pages are cited here.

Every statement was checked against the operator's live page on **2026-11-23**. Operators changed these pages several times during 2026: Google added a dedicated guide, a Search Console control, and a report; Microsoft announced new preference signals. Fetch the page again before relying on a row in a decision, and record the retrieval date in the evidence ledger. No operator guarantees inclusion, citation, or placement.

## Eligibility checklist

Run these checks before any content or off-site work. A blocked crawler makes everything else irrelevant.

1. Read the live `robots.txt` and confirm it does not disallow `Googlebot`, `Bingbot`, `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`, or `Claude-User` for pages that should be eligible.
2. Confirm the CDN or web application firewall is not blocking those crawlers. OpenAI and Perplexity publish IP ranges and recommend allowing them, so check the IP allowlist as well as the user-agent rules.
3. Confirm the priority pages are indexed in Google and Bing, return the content without requiring client-side interaction, and have a canonical URL.
4. Check page-level directives. `nosnippet`, a low `max-snippet`, `noindex`, `NOARCHIVE`, and `NOCACHE` each restrict AI use on at least one engine.
5. In Google Search Console, confirm the effective Search generative AI setting for each priority URL. Inclusion is the default, but a child property such as a URL-prefix property inherits from its closest configured parent and can override it. A change generally takes a few days to apply.
6. Treat training crawlers as a separate decision. Blocking `GPTBot` or `ClaudeBot` does not remove a site from those engines' search answers, and blocking `Google-Extended` does not affect Google Search or its AI features. `Google-Extended` does govern grounding in the Gemini app, so ask which Google surface matters before judging a block.
7. After a `robots.txt` change, wait before retesting. OpenAI and Perplexity say their systems take about 24 hours. The other operators give no figure; confirm with crawl logs or the operator's own tools instead of assuming the same delay.

## Google Search: AI Overviews and AI Mode

| Topic | What Google states |
|---|---|
| Eligibility | A page must be indexed and eligible to be shown in Google Search with a snippet. The AI features page says there are no additional technical requirements. The newer AI optimization guide adds that a site must be included in Search generative AI features in Search Console. |
| Crawler | Googlebot. There is no separate crawler for AI Overviews or AI Mode. |
| Search generative AI control | A setting in Search Console, available worldwide since 2026-08-31. A property inherits the setting from its closest parent that changed it, and an owner can override it on a child property. Google says the control is not used as a ranking or inclusion signal for other parts of Search and does not affect AI training. |
| `Google-Extended` | Controls use for Gemini training and for grounding in Gemini Apps and Vertex AI. It does not affect inclusion in Google Search and is not a ranking signal. |
| `nosnippet`, `max-snippet` | Both apply to AI Overviews and AI Mode. `nosnippet` also prevents content from being used as a direct input; `max-snippet` limits how much may be used. |
| Stated as unnecessary | `llms.txt` ("Google Search ignores them"), breaking content into small pieces for AI, writing in a special way for AI, and special schema.org markup. |
| Stated as unhelpful or prohibited | Seeking inauthentic mentions across the web "isn't as helpful as it might seem". Creating pages for every query variation, including fan-out queries, primarily to manipulate rankings or AI responses violates the scaled content abuse policy. The spam policies cover attempts to manipulate generative AI responses. |
| Stated as mattering | Helpful, reliable, non-commodity content; crawlability; structured data that matches the visible text. |
| Position on the discipline | Optimizing for generative AI search "is optimizing for the search experience, and thus still SEO." |
| Measurement | The Search Console generative AI performance report, worldwide since 2026-08-31. Its help page describes impressions by page, country, device, and date. It does not describe clicks, queries, or a split between AI Overviews and AI Mode. The report does not appear until a site has enough impressions in AI features, so a missing report is not a measured zero. |

## OpenAI: ChatGPT search

| Topic | What OpenAI states |
|---|---|
| Eligibility | Allow `OAI-SearchBot` and confirm the host or CDN allows OpenAI's published search-bot IP addresses. |
| Ranking | ChatGPT "ranks search results using multiple factors". Placement is not guaranteed. No factor list is published. |
| `OAI-SearchBot` | Governs search. A site that opts out is not shown in search answers but can still appear as a navigational link. |
| `GPTBot` | Governs training of foundation models. Independent of search inclusion. |
| `ChatGPT-User` | Fetches pages for user-initiated actions. OpenAI says `robots.txt` rules may not apply to it, and that it is not used to decide whether content appears in search. |
| Timing | A `robots.txt` update can take about 24 hours to take effect for search. |
| Measurement | Business Hub insights show aggregate mentions and website clicks over the past 28 days after a claim and identity verification. For an online business a mention counts only when ChatGPT references the business's website; the brand name alone does not count. A blank metric can mean the activity is below the reporting threshold, still being collected, or unavailable; OpenAI says it does not necessarily mean zero. |
| Claiming a profile | OpenAI states that claiming a profile or disputing ownership does not change its visibility in ChatGPT. |

## Perplexity

| Topic | What Perplexity states |
|---|---|
| `PerplexityBot` | Surfaces and links sites in Perplexity search results. Not used to crawl content for foundation models. Perplexity recommends allowing it in `robots.txt` and allowing its published IP ranges. |
| `Perplexity-User` | Fetches a page when a user asks. It generally ignores `robots.txt` because the user requested the fetch. |
| Timing | Changes can take up to 24 hours to be reflected. |
| Content guidance, measurement | None found on the crawler documentation. |

## Anthropic: Claude web search

| Topic | What Anthropic states |
|---|---|
| `ClaudeBot` | Collects content that may contribute to model training. Blocking it signals that future material should be excluded from training datasets. |
| `Claude-SearchBot` | Analyzes content to improve search result quality. |
| `Claude-User` | Retrieves pages when a user asks Claude a question. Blocking it may reduce visibility for user-directed web search. |
| `robots.txt` | Anthropic's bots honor `robots.txt`, including the user-initiated one, and support the non-standard `Crawl-delay` extension. |
| Content guidance, measurement | None found on the crawler article. |

## Microsoft: Bing and Copilot

| Topic | What Microsoft states |
|---|---|
| Foundation | Bing and Copilot search experiences rely on the same crawling, indexing, and ranking foundation as traditional search. |
| `robots.txt` and `NOINDEX` | `robots.txt` controls crawl access, not indexing. Use `NOINDEX` when a URL should not appear in Bing search, Copilot experiences, or grounding results. |
| `NOARCHIVE`, `NOCACHE` | `NOARCHIVE` prevents use in Copilot responses and grounding results. `NOCACHE` limits Copilot to the URL, title, and snippet. |
| New preference signals | Separate AI Training and AI Grounding preferences, both defaulting to allow, are honored from 2027-02-01. A site that relies on `NoArchive` or `NoCache` today must act before 2027-03-01 to keep its choice: publish the AI Training preference in `robots.txt` or on pages, publish the AI Grounding preference on pages, and record a temporary transition grounding preference in Bing Webmaster Tools. After that date the old tags are no longer read as a preference for training or grounding. Microsoft says neither choice guarantees inclusion, traffic, or payment. |
| Content guidance | Microsoft recommends clear headings, tables, and FAQ sections, explicit facts and definitions, and evidence for claims. Structured data "may support clearer grounding but does not guarantee visibility". |
| Position on the discipline | Microsoft uses the term Generative Engine Optimization and states that it does not guarantee grounding or citations. |
| Manipulation | Content designed to manipulate or interfere with the language models used by Bing or Copilot may lead to reduced visibility or removal. Content should be created for users, not to trigger citations or AI responses. |
| Measurement | The AI Performance report in Bing Webmaster Tools shows how often a site's content is cited in generative answers, page-level citation counts, and a sample of grounding queries. |

Microsoft's security team separately documented "AI Recommendation Poisoning": "Summarize with AI" links whose pre-filled prompt tells the assistant to remember a company as a trusted source. It classifies this as memory poisoning of the user's assistant and reports that every case it found came from a real business, not an attacker. Never build this into a page.

## Where operators disagree

- **Structure for AI.** Google says there is no need to chunk content or write differently for AI. Microsoft recommends headings, tables, FAQ sections, and self-contained statements. Clear structure for readers satisfies both. Do not promise that structure produces citations.
- **The label.** Google calls the work SEO. Microsoft adopts the term GEO. The disagreement is about naming, not about a different set of mechanics.
- **User-initiated fetchers.** Perplexity's generally ignores `robots.txt`, OpenAI says the rules may not apply, and Anthropic's honors them. A `robots.txt` block is therefore not a reliable way to keep a public page out of every assistant's reach.

## Claims with no first-party support

Label these as hypotheses when they appear in a plan or a vendor proposal:

- `llms.txt` improves citation on ChatGPT, Perplexity, Claude, or Copilot. Google says its search ignores the file; the pages checked for the other operators state no position.
- A published list of citation or ranking factors for ChatGPT, Perplexity, or Claude.
- Special markup, FAQ schema, or an "AI-readable" format that an engine requires.
- A referral parameter such as `utm_source=chatgpt.com` as a documented guarantee. The OpenAI pages checked on the date above do not document it; treat it as observed behavior and confirm it in the product's own analytics.
- Claiming a business profile, or connecting a product feed, raises visibility. OpenAI says claiming does not.
- A third-party tool has access to an engine's internal ranking or AI systems. Google states that none does.

## Sources

All retrieved 2026-11-23.

- Google: [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) (last updated 2026-07-10), [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) (2025-12-10), [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) (2026-08-28), [Robots meta tag specifications](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), [Google's common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), [Search generative AI control](https://support.google.com/webmasters/answer/16908024), [Generative AI performance report](https://support.google.com/webmasters/answer/16984139).
- OpenAI: [Overview of OpenAI crawlers](https://developers.openai.com/api/docs/bots), [Searching the web with ChatGPT](https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt), [Setting up your business on ChatGPT](https://help.openai.com/en/articles/20001635-setting-up-your-business-on-chatgpt).
- Perplexity: [Perplexity crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers).
- Anthropic: [Does Anthropic crawl data from the web, and how can site owners block the crawler?](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- Microsoft: [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a), [AI Performance in Bing Webmaster Tools](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) (2026-02-10), [Preferences for training and grounding](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/) (2026-10-30), [AI Recommendation Poisoning](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) (2026-02-10).
