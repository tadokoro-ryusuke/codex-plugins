# Ethics, Trust, and Compliance Guardrails

## Contents

1. [Operating rule](#operating-rule)
2. [Japanese disclosure](#japanese-disclosure)
3. [Personal data and tracking](#personal-data-and-tracking)
4. [Platform automation](#platform-automation)
5. [Demand tests and waitlists](#demand-tests-and-waitlists)
6. [Reviews, rankings, and proof](#reviews-rankings-and-proof)
7. [Content, SEO, and AI](#content-seo-and-ai)
8. [Community and UGC](#community-and-ugc)
9. [Preflight checklist](#preflight-checklist)

## Operating rule

Protect the customer's ability to make an informed choice. Apply the stricter applicable requirement among law, platform policy, community norms, and the promise made to the user. Treat this reference as an operational checklist, not legal advice. Escalate material uncertainty to qualified counsel.

## Japanese disclosure

The [Consumer Affairs Agency stealth-marketing FAQ](https://www.caa.go.jp/policies/policy/representation/fair_labeling/faq/stealth_marketing/) explains that advertiser-controlled representations must be recognizable as advertising.

- Mark sponsored, paid, gifted, affiliate, and otherwise incentivized content clearly where users will notice before acting.
- Tell creators and affiliates what must be disclosed, but do not script a falsely independent opinion.
- Disclose the founder's affiliation when recommending the product in a community.
- Keep evidence of briefing, compensation, product provision, approval, and published disclosure.
- Do not hide disclosure among hashtags, behind a fold, or on a profile when the endorsement appears elsewhere.

Review current Japanese rules and guidance for the actual campaign, product, and jurisdiction.

## Personal data and tracking

The [Personal Information Protection Commission guidelines](https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/) require an appropriate purpose of use and handling of personal information. Apple separately requires [App Tracking Transparency](https://developer.apple.com/documentation/apptrackingtransparency) authorization for covered cross-app or cross-site tracking.

- State why email, interview data, analytics identifiers, or application data are collected.
- Collect only what the declared test and follow-up require.
- Record consent language and version, lawful access, retention, deletion, and processors.
- Separate essential service analytics from advertising or cross-context tracking.
- Respect consent denial; do not create a degraded or deceptive flow to force acceptance.
- Avoid putting sensitive or identifying data in URLs, UTM fields, screenshots, prompts, or shared artifacts.
- Define how waitlist users can unsubscribe and how interview or beta data can be deleted.
- Review international transfers, children's data, and sensitive categories when applicable.

Do not infer that a platform SDK is compliant merely because it is popular.

## Platform automation

The [X automation rules](https://help.x.com/en/rules-and-policies/x-automation) prohibit automated likes and aggressive or indiscriminate automated actions; AI reply bots require prior written approval. The [X authenticity policy](https://help.x.com/en/rules-and-policies/authenticity) also covers bulk or aggressive manual behavior.

- Use automation for drafting, scheduling owned posts, classification, and internal research only when allowed.
- Require a human to review direct replies, claims, tone, disclosure, and recipient relevance.
- Do not automate likes, follow churn, unsolicited replies, or bulk DMs.
- Do not use many accounts to manufacture attention, consensus, testimonials, or engagement.
- Rate-limit legitimate operations and provide an immediate stop mechanism.
- Recheck current rules before launching; platform policies change.

Manual spam is still spam. Personalization fields do not turn an unsolicited bulk message into a genuine relationship.

## Demand tests and waitlists

- Make a fake-door or preorder test truthful at the point of commitment.
- Clearly distinguish available now, beta, waitlist, planned, and conceptual functionality.
- Explain what happens after signup and how frequently follow-up will occur.
- Do not charge unless delivery, timing, refund, and support terms are clear.
- Never create fake scarcity, countdowns, users, orders, or capacity constraints.
- Do not imply that a waitlist place guarantees access, price, or release timing unless it does.
- Use qualitative follow-up to learn why a person acted; an email alone is weak evidence.

When a test could materially disappoint users, prefer a prototype, refundable deposit, or explicit research invitation over deception.

## Reviews, rankings, and proof

Apple's [ratings and reviews guidance](https://developer.apple.com/app-store/ratings-and-reviews/) supports requesting ratings at an appropriate satisfaction moment.

- Ask for an honest review after value, not specifically a positive review.
- Do not buy, fabricate, gate, or selectively suppress negative reviews.
- Disclose incentives and ensure they comply with store and consumer rules.
- Preserve the denominator and date for claims such as conversion, users, ratings, or ranking.
- Say whether “users” means installs, registrations, activated users, active users, retained users, or payers.
- Do not present revenue as profit; include fees and relevant variable costs.
- Mark forecasts, targets, and founder reports as such.

Use testimonials only with permission and enough context to avoid a misleading typicality claim.

## Content, SEO, and AI

Google's [generative-AI guidance](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) and [spam policies](https://developers.google.com/search/docs/essentials/spam-policies) reject scaled content created mainly to manipulate ranking when it adds little value.

- Use AI to assist research, transcription, structure, and variants.
- Verify factual, legal, medical, financial, comparative, and performance claims.
- Add original experience, data, methodology, tools, examples, or editorial judgment.
- Cite primary sources and record update dates.
- Respect copyright, trademark, quotation, image, music, dataset, and community rules.
- Do not impersonate customers, experts, journalists, or competitors.
- Avoid publishing near-duplicate pages for every keyword or geography without distinct user value.
- Provide a correction and removal process.

Do not promise placement in search or generative answers. Technical crawl eligibility does not guarantee recommendation.

## Community and UGC

- Publish community rules, reporting routes, enforcement actions, and appeal or support paths appropriate to the product.
- Decide how to handle harassment, sexual content, minors, self-harm, illegal content, impersonation, spam, copyright, and private information before scale.
- Make founder-seeded content identifiable; do not invent people or activity.
- Obtain rights for imported, scraped, user, or partner content.
- Let users preview shared content and remove sensitive fields by default.
- Measure safety load and response time alongside growth.
- Stop acquisition when moderation, support, or reliability capacity is exceeded.

Specialized products may create additional consumer, payment, health, finance, employment, accessibility, export, or age-assurance obligations.

## Preflight checklist

Before launch, confirm:

- [ ] Every material performance claim has a source, denominator, period, and caveat.
- [ ] Sponsored, affiliate, gifted, and founder relationships are visible.
- [ ] The landing page distinguishes live, beta, waitlist, and planned features.
- [ ] Purpose of data collection, consent, privacy notice, retention, and deletion are defined.
- [ ] Analytics and advertising SDKs have been reviewed for consent and data flow.
- [ ] Platform advertising, automation, contest, review, and community rules are current.
- [ ] No fabricated users, activity, scarcity, reviews, or rankings appear.
- [ ] Sharing defaults protect private data and recipient expectations.
- [ ] Support, refund, moderation, incident, and takedown routes are staffed.
- [ ] The campaign has a budget, rate limit, guardrails, and stop control.
- [ ] A named owner will check complaints and safety signals during the campaign.
- [ ] Material legal uncertainty has been escalated instead of guessed.
