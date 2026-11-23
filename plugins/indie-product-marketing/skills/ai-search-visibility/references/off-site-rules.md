# Off-Site Work: Routes and Rules

## Contents

1. [The line every regime draws](#the-line-every-regime-draws)
2. [Choose a route](#choose-a-route)
3. [Tactic rulings](#tactic-rulings)
4. [Disclosure in community posts](#disclosure-in-community-posts)
5. [Enforcement examples](#enforcement-examples)
6. [Limits of this reference](#limits-of-this-reference)
7. [Sources](#sources)

## The line every regime draws

AI answers draw on what third-party pages say about a product, so off-site work is where the pressure to cut corners is highest. Platform rules, search spam policies, and consumer law in Japan, the United States, the European Union, and the United Kingdom converge on one line:

**Content the business wrote, directed, paid for, or rewarded must be recognizable as the business's own. A genuinely independent opinion stays independent only if the business did not shape it.**

The regimes test this differently: editorial control over the content in Japan, a material connection in the United States, a hidden commercial purpose in the EU and the UK. A neutral request that leaves the content to the reviewer does not turn an honest review into the business's speech. Where this file is stricter than a cited rule, it says so.

Apply the stricter requirement among law, platform policy, community rules, and the promise made to users. This file is an operational checklist, not legal advice. Escalate material uncertainty to qualified counsel. The rulings below were checked against the cited sources on 2026-11-23.

## Choose a route

For each third-party source tied to a priority buyer question, first read what it says about the product: absent, inaccurate, outdated, incomplete, or already fair. Then choose one route. The four-route split follows the Own / Claim / Earn / Contest framework described in the Discovered Labs case study listed under Sources; "leave" is added here because it is often the right answer.

| Route | The source is | Legitimate actions |
|---|---|---|
| **Own** | A page or account the business controls: its site, documentation, pricing, changelog, own social accounts | Correct facts, publish the missing page, keep numbers consistent everywhere |
| **Claim** | A profile the business is entitled to manage: directories, review sites, marketplaces, operator business profiles | Claim it, complete the facts, respond to reviews. Never review your own product |
| **Earn** | Something a third party decides: a review, a comparison, a community answer, press, a partner page | Give them something worth including, ask openly, disclose the relationship, accept a no |
| **Contest** | A statement about the product that is factually wrong or out of date | Ask the author to correct the fact with evidence; on Wikipedia, propose the change on the talk page |
| **Leave** | Accurate, irrelevant, closed to promotion, or reachable only by a prohibited route | Record the decision and move on |

Record each source and decision in `../assets/source-ledger.md`. Measure which sources the product's own prompts actually cite before choosing where to work; do not assume any single platform.

## Tactic rulings

| Tactic | Ruling | Basis |
|---|---|---|
| A founder or employee answers questions in a community and states the relationship in the post | Allowed with disclosure. The community's own rules come first | Japan: a post by someone whose role is to promote sales is the business's own representation (Consumer Affairs Agency operating standard, part 2-1(1)), and stating an employer alone does not necessarily make that clear (CAA Q&A Q12). United States: a material connection must be disclosed clearly and conspicuously (16 CFR 255.5), and listing an employer on a profile page is not enough (FTC Endorsement Guides FAQ). |
| An agency, contractor, or friend posts about the product without disclosing the relationship | Prohibited | Japan: a post the business asked a third party to make is the business's representation (operating standard, part 2-1(2)); undisclosed, it violates the stealth-marketing designation, and the order is addressed to the advertiser (CAA Q&A Q1). United States: 16 CFR 255.5; intermediaries such as agencies may be liable (16 CFR 255.1(f)), and delegating a program does not relieve the advertiser of responsibility (FTC FAQ). EU: falsely representing oneself as a consumer (Unfair Commercial Practices Directive, Annex I, point 22). UK: commissioning a fake review or one that conceals an incentive (DMCC Act 2024, Schedule 20, paragraph 13). |
| Posting from purchased or transferred accounts; voting with several accounts; coordinated upvotes | Prohibited by platform rules and by this skill | Reddit's User Agreement bars licensing, selling, or transferring an account without written approval, and Reddit's help center describes voting from several accounts and coordinated voting as prohibited manipulation (excerpt only; see Limits). United States: 16 CFR 465.8 reaches fake indicators of social media influence when the buyer knew or should have known they were fake and uses them to misrepresent influence for a commercial purpose, so not every coordinated vote is a federal violation. |
| Asking eligible customers for an honest review, with no incentive | Allowed | United States: generalized solicitations to purchasers are carved out (16 CFR 465.2(d)). Trustpilot requires invitations to be fair, neutral, and unbiased, and tells businesses not to invite people with a special relationship to the business, such as close family, people working in or with it, or shareholders. Ask all eligible customers alike; inviting only those expected to be happy is not a fair invitation. Check each platform's rules on who may be invited and how often. |
| Offering an incentive for a review | Restricted | Japan: a modest reward for posting, with no exchange of any kind about the content, is normally not the business's representation; requiring a rating or favorable wording makes it one (CAA Q&A on review incentives; operating standard, part 2-2). United States: no compensation conditioned on a particular sentiment (16 CFR 465.4), and the FTC adds that failing to disclose an incentive could violate the FTC Act even when no sentiment is required. UK: a review must not conceal that it was incentivized. Trustpilot does not allow incentivized reviews. G2 labels incentivized reviews and caps any incentive at USD 100. Offer an incentive only where the platform allows it and the review will carry the platform's label. |
| Quoting customer reviews on the product's own site, unaltered and without picking favorites | Allowed | Japan: quoting third-party content as it is, without arbitrary selection or changes, is not the business's representation; a random sample of survey answers is the example given (CAA Q&A Q10). |
| Selecting favorable reviews, quoting only the positive part, or reusing posts the business requested | Allowed only when shown as the business's own selection | Japan: choosing favorable answers or quoting only the good points makes the quotation the business's representation, which must be made clear (CAA Q&A Q10). UK: publishing consumer reviews or review information in a misleading way is banned, and a publisher must take reasonable and proportionate steps against fake reviews and reviews that conceal an incentive (DMCC Act 2024, Schedule 20, paragraph 13). Do not present a selection as the whole body of reviews. |
| Paying for inclusion or position in a third-party list or article | Allowed only with a label readers can see **and** `rel="sponsored"` or `rel="nofollow"`, and never to borrow the host's ranking | Google: exchanging money, goods, or services for links that pass ranking credit is link spam; qualified links are not a violation. Google's site reputation policy separately covers third-party content placed on a host mainly because of that host's established ranking signals, so ask what the placement is for before agreeing to it. The attribute is invisible to readers, so the visible label is what satisfies the Japanese designation (wording such as 「広告」「PR」, operating standard, part 3), 16 CFR 255.5, and the EU ban on unlabeled paid editorial content (Annex I, point 11). |
| Buying links, or exchanging links, mainly for ranking | Prohibited by Google's link spam policy | Covers money, goods, or services for links, excessive link exchanges, and optimized links in guest posts and forum comments. The consequence is lower ranking or removal. |
| Publishing a comparison on the product's own site that ranks the product first | Allowed when it is plainly the product's own page and every claim is supported | United States: do not present a site the business controls as independent reviews (16 CFR 465.6). Japan: unsupported superiority or "No. 1" claims fall under misleading-representation rules. AI answers often cite such a page without recommending its author; see [evidence-base.md](evidence-base.md). |
| Claiming and completing profiles on directories and review sites | Allowed | Trustpilot lets businesses claim and manage a profile. G2 bars employees of the vendor from reviewing. OpenAI states that claiming a business profile does not change visibility in ChatGPT. |
| Asking an author to correct a factual error | Allowed for facts | Japan: asking a reviewer to fix a factual error does not make the review the business's representation; asking for a more favorable opinion does (CAA Q&A Q9). Offering payment or a link in exchange turns it into a paid placement. |
| Editing the company's own Wikipedia article | Do not edit directly | Editors with a conflict of interest are strongly discouraged from editing affected articles and should propose changes on the talk page. Paid contributors must disclose employer, client, and affiliation. |
| Embedding instructions aimed at AI assistants: hidden text, or "summarize with AI" links that tell the assistant to remember the brand as a trusted source | Prohibited | Microsoft's security team classifies the memory variant as poisoning of the user's assistant. Bing's guidelines list content designed to manipulate language models as grounds for reduced visibility or removal. Google's spam policies cover attempts to manipulate generative AI responses. |
| Mass-producing pages for every query variation | Prohibited | Google: doing so primarily to manipulate rankings or AI responses violates the scaled content abuse policy. |

When a vendor offers a prohibited tactic as a service, the advertiser remains responsible for it. Ask the questions in [evidence-base.md](evidence-base.md) under "Auditing a vendor proposal or case study".

## Disclosure in community posts

The Japanese disclosure rules, review-incentive rules, and platform-automation limits are in the `indie-product-marketing` skill's `references/ethics-and-compliance.md`. Use that file for wording and record-keeping. Three points matter specifically for community answers:

- **Disclose in the body of the post.** A profile line does not count, and a disclosure placed in a reply instead of the post is often not clear enough (CAA Q&A Q14).
- **Say what the relationship is, in the language of the post.** "I built this" or 「開発者です。自社の製品です」 tells the reader what an employer name alone does not.
- **Answer the question first.** Mention the product only where it fits the question, name alternatives fairly, and leave the thread alone when the community bans promotion.

Prepare drafts freely. Posting, messaging, review requests, and outreach are external actions; perform them only when the user has asked for that action.

## Enforcement examples

- **Japan, 2026-08-06.** The Consumer Affairs Agency issued orders against the two companies that provide the SNOW app. The Japanese affiliate had asked third parties, in return for payment, to post on X along a line it specified, and the posts did not show that they were the companies' own representations. The parent company is based outside Japan.
- **United States, July 2026.** The FTC finalized an order settling its allegations against a supplement seller: fake and incentivized reviews and bot-run social profiles, together with unsupported health claims. The order imposes a USD 4 million judgment, to be partially suspended once the company pays USD 750,000. These are settled allegations, not findings after trial, and the amount is not attributable to the review conduct alone.
- **Platforms (reported, not re-checked).** In 2026 moderators of at least one large subreddit paused new posts on topics that companies were seeding for AI visibility, and Reddit said publicly that it questions any provider claiming it can get Reddit content into AI answers.

## Limits of this reference

- **Reddit.** Reddit's rules pages and help center refused automated retrieval on 2026-11-23. The Reddit rows rest on the User Agreement as reproduced in Reddit's own policy filing with the New York Attorney General and on help-center excerpts returned by search, not on the full pages. Read the live Reddit Rules and the target community's rules before any post.
- **Business buyers.** The Japanese designation, the EU directive, and the UK schedule are written around consumers. How they apply to a product sold only to businesses was not reviewed. The platform rules and search policies apply regardless.
- **Other markets.** Only Japan, the United States, the EU, and the UK were reviewed.
- **Currency.** Rules in this area changed during 2024–2026. Re-read the source before a campaign.

## Sources

Retrieved 2026-11-23.

- Japan, Consumer Affairs Agency: [designation](https://www.caa.go.jp/policies/policy/representation/fair_labeling/public_notice/assets/representation_cms216_230328_07.pdf) (in force 2023-10-01), [operating standard](https://www.caa.go.jp/policies/policy/representation/fair_labeling/guideline/assets/representation_cms216_230328_03.pdf), [stealth-marketing Q&A](https://www.caa.go.jp/policies/policy/representation/fair_labeling/faq/stealth_marketing/), [order of 2026-08-06](https://www.caa.go.jp/notice/assets/representation_cms207_260806_02.pdf).
- United States: [16 CFR 255.1](https://www.law.cornell.edu/cfr/text/16/255.1), [255.5](https://www.law.cornell.edu/cfr/text/16/255.5), [465.2](https://www.law.cornell.edu/cfr/text/16/465.2), [465.4](https://www.law.cornell.edu/cfr/text/16/465.4), [465.5](https://www.law.cornell.edu/cfr/text/16/465.5), [465.6](https://www.law.cornell.edu/cfr/text/16/465.6), [465.8](https://www.law.cornell.edu/cfr/text/16/465.8); FTC [Endorsement Guides FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [reviews rule Q&A](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers), [TruHeight final order](https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-approves-final-order-against-truheight-deceptive-unsubstantiated-advertising-supplements-kids).
- EU and UK: [Unfair Commercial Practices Directive, Annex I](https://www.legislation.gov.uk/eudr/2005/29/annex/I); [Digital Markets, Competition and Consumers Act 2024, Schedule 20](https://www.legislation.gov.uk/ukpga/2024/13/schedule/20).
- Google: [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies), [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).
- Microsoft: [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a), [AI Recommendation Poisoning](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/).
- Platforms: [Reddit User Agreement, as filed with the New York Attorney General](https://ag.ny.gov/sites/default/files/social-media-policy-report/2026-q1q2-reddit-inc-policy-1.pdf); [Wikipedia: Conflict of interest](https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest); [Wikipedia: Paid-contribution disclosure](https://en.wikipedia.org/wiki/Wikipedia:Paid-contribution_disclosure); [Trustpilot guidelines for businesses](https://corporate.trustpilot.com/legal/for-businesses/guidelines-for-businesses); [G2 community guidelines](https://legal.g2.com/community-guidelines); OpenAI, [Setting up your business on ChatGPT](https://help.openai.com/en/articles/20001635-setting-up-your-business-on-chatgpt).
- Framework credit: Discovered Labs, [Granola case study](https://discoveredlabs.com/case-studies/granola) (Own / Claim / Earn / Contest).
