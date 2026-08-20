# Metrics and Experiments

## Contents

1. [Measurement contract](#measurement-contract)
2. [Event and source model](#event-and-source-model)
3. [Funnel metrics](#funnel-metrics)
4. [Retention and product-market fit](#retention-and-product-market-fit)
5. [Revenue and unit economics](#revenue-and-unit-economics)
6. [Experiment design](#experiment-design)
7. [Small-sample rules](#small-sample-rules)
8. [Decision rules](#decision-rules)
9. [Reporting](#reporting)
10. [Common metric traps](#common-metric-traps)

## Measurement contract

Define before launching an experiment:

- **Entity:** user, account, device, installation, lead, order, or subscription.
- **Eligibility:** who enters the denominator and when.
- **Exposure:** what proves the user received the treatment.
- **Conversion window:** how long the outcome may occur after exposure.
- **Primary outcome:** the one metric that decides the test.
- **Guardrails:** quality, retention, revenue, refunds, reliability, privacy, or support.
- **Attribution:** source, campaign, referrer, promo code, platform attribution, or randomized assignment.
- **Cohort:** acquisition date, source, segment, geography, device, or offer.
- **Decision date:** when results will be evaluated.
- **Action rule:** pass, revise, stop, or collect more evidence.

Keep definitions stable across reports. If a definition changes, version it and avoid comparing incompatible periods.

If no baseline exists, run a short instrumentation or feasibility pilot before an optimization test. Use an absolute behavioral threshold tied to the decision, such as qualified interviews completed, prototype users reaching first value, deposits, or repeated use. Do not manufacture an industry benchmark to fill the blank. Label the cohort exploratory and promote it to a baseline only after verifying event quality, source, product version, and eligibility.

## Event and source model

### Minimum event taxonomy

Use names that describe completed behavior:

| Stage | Example event | Required properties |
|---|---|---|
| Reach | `campaign_impression` when available | source, campaign, creative, audience |
| Visit | `landing_viewed` or store impression | source, campaign, landing variant |
| Intent | `primary_cta_clicked` | offer, variant |
| Lead | `qualified_lead_submitted` | segment, qualification, consent version |
| Signup | `account_created` or `install_attributed` | source, campaign, platform |
| Activation | product-specific completed value event | time from signup, template/path |
| Retention | repeated core event | cohort, interval, active definition |
| Revenue | `purchase_completed` or `subscription_renewed` | gross revenue, net proceeds, product, currency |
| Referral | `share_completed`, `invite_accepted` | channel, sender cohort, recipient cohort |
| Quality | `refund_requested`, `crash`, `support_ticket` | reason, severity |

Do not collect personal data merely because it may be useful. Use the minimum needed and document purpose, consent, retention, and access.

### Source taxonomy

Store both a normalized source and raw platform fields:

- `source_system`: search, social, community, partner, referral, direct, store browse, store search.
- `source_name`: Google, X, Instagram, Product Hunt, partner name, customer referral.
- `medium`: organic, paid, email, affiliate, in-product, QR, event.
- `campaign`: stable human-readable campaign name.
- `content`: creative or message variant.
- `term`: keyword or audience when allowed.
- `first_touch` and `latest_touch` where needed.
- Platform attribution IDs subject to consent and privacy rules.

Preserve “unknown” rather than silently classifying unattributed users as direct.

## Funnel metrics

Use the same cohort and denominator within each rate:

- `visit rate = qualified visits / qualified reach`
- `intent rate = primary CTA actions / eligible visits`
- `lead rate = qualified leads / eligible visits`
- `signup rate = completed signups or installs / eligible visits`
- `activation rate = users completing the value event / eligible new users`
- `paid conversion = new paying customers / eligible activated users`
- `referral rate = users completing a qualifying share or invite / eligible active users`
- `recipient activation = activated referred users / eligible referred recipients`

Report counts beside rates. A 50% rate from two users is not equivalent to 50% from two thousand.

### Time-to-value

Measure median and distribution, not only the average:

- Time from first visit to signup.
- Time from signup to activation.
- Number of steps to first value.
- Percentage reaching value within the target window.

Long-tail failures can hide behind a good average.

## Retention and product-market fit

### Choose the natural interval

Match retention to expected use:

- Daily social or habit product: D1, D7, D30 and rolling active behavior.
- Weekly workflow: W1, W4, W8.
- Monthly finance or reporting product: M1, M3, M6.
- Episodic product: return at the next triggering event or repeat task.

Define what “active” means through value, not app opens alone.

### Cohort retention

`retention at N = cohort members completing the core value event in interval N / eligible cohort members`

Inspect curves by source, segment, version, geography, and activation path. A flattening curve may indicate a retained segment; compare its size, value, and reachability.

### PMF evidence bundle

Use multiple signals:

- Stable or improving retention for the target segment.
- Repeated core-value behavior.
- Willingness to pay, renew, or accept price increases.
- Organic referrals or unsolicited recommendations.
- Qualitative dependency on the product's outcome.
- A PMF survey among users who have experienced value.
- Pull that outpaces current support or delivery capacity.
- A market large and reachable enough for the founder's objective.

The Sean Ellis “very disappointed without the product” threshold is a practitioner heuristic. Use it to identify the segment and benefit that love the product; do not use 40% as a legal verdict on PMF.

## Revenue and unit economics

### Cost metrics

- `CPL = attributable acquisition cost / qualified leads`
- `CPI = attributable acquisition cost / incremental installs`
- `CAC = attributable sales and marketing cost / new paying customers`
- `activated CAC = attributable acquisition cost / activated new users`
- `retained CAC = attributable acquisition cost / new users retained at interval N`

Include media, creative, contractor, affiliate, sales-tool, and allocated founder costs when the decision requires fully loaded economics. State what is included.

### Contribution

Calculate by cohort and period:

`gross contribution = net revenue - platform fees - refunds - variable infrastructure - variable support/fulfillment - partner payouts`

Keep fixed and variable infrastructure separate. A social or AI product may have user-level cost that makes large free cohorts economically dangerous.

### Payback

`payback months = CAC / average monthly gross contribution per new customer`

Show a cohort table rather than assuming all customers behave like the average.

### Lifetime value

For a stable subscription cohort, a rough steady-state estimate may be:

`LTV ≈ average revenue per account × gross margin / periodic logo churn`

This formula is fragile when churn is volatile, cohorts are young, expansion is material, billing intervals differ, or survival is non-geometric. Prefer observed cumulative gross contribution by cohort and sensitivity ranges.

### Maximum acquisition cost

Derive from constraints:

- Desired payback window.
- Expected gross contribution during that window.
- Cash availability.
- Refund and fraud risk.
- Support and operational capacity.
- Uncertainty margin.

Do not import a generic LTV:CAC ratio or fixed CPA without explaining why it fits the business.

## Experiment design

### Write the hypothesis

Use:

> Because **[evidence]**, changing **[one controllable variable]** for **[segment]** should improve **[primary metric]** from **[baseline]** to **[target]** within **[window]**, without worsening **[guardrail]** beyond **[limit]**.

### Choose the design

- **Randomized A/B:** use when traffic and tooling support comparable control and treatment groups.
- **Holdout or geo test:** use when channel or market exposure can be isolated.
- **Pre/post with matched baseline:** use when randomization is unavailable; explicitly list confounders.
- **Sequential smoke test:** use to reject severe mismatch or recruit learning participants, not to estimate small lifts precisely.
- **Qualitative usability test:** use to locate mechanisms behind activation failures.
- **Concierge pilot:** use to test outcome value before automating delivery.

### Change one causal bundle

Some variables form an inseparable bundle, such as a new audience and message specifically written for it. Name the bundle. Do not change audience, offer, price, landing experience, and onboarding together and then attribute the result to the creative.

### Set guardrails

Examples:

- Activation and retention.
- Refund or unsubscribe rate.
- Gross contribution.
- Crash or error rate.
- Support contacts per activated user.
- Spam reports, blocks, or negative feedback.
- Privacy or consent failures.
- UGC moderation incidents.

## Small-sample rules

When volume is low:

1. Prefer large, decision-relevant changes over color or wording microtests.
2. Combine quantitative behavior with interviews and session observation.
3. Predeclare the minimum sample or time window.
4. Report confidence intervals or plausible ranges when possible.
5. Label evidence as directional when it cannot detect the desired effect.
6. Do not repeatedly peek at fixed-horizon significance and stop on a favorable fluctuation.
7. Do not run many variants that divide already sparse traffic.
8. Repeat promising results in a new period or cohort before scaling.

Platform learning matters. Meta recommends enough budget over at least seven days, while Google notes that high-volume, longer experiments are more likely to become conclusive. These are platform guidelines, not universal minimums; the required window depends on conversion delay and volume.

## Decision rules

Define all four outcomes:

- **Pass:** primary outcome meets the target and guardrails hold.
- **Revise:** evidence supports the problem but points to a different segment, message, offer, or product path.
- **Stop:** the primary threshold fails after credible exposure, a guardrail fails materially, or economics cannot work.
- **Continue collecting:** only when the predeclared design says the current sample is insufficient and extending does not introduce opportunistic bias.

Every result should create one of:

- A new default.
- A follow-up experiment.
- A product fix.
- A retired hypothesis.
- A data-quality repair.

## Reporting

### Experiment card

Include:

- ID, owner, dates, and status.
- Segment, channel, and lifecycle stage.
- Evidence and hypothesis.
- Control/baseline and treatment.
- Primary metric, guardrails, and sample/window.
- Budget and founder hours.
- Raw counts, rates, intervals, and source quality.
- Result classification and confidence.
- Decision and next action.

### Weekly scorecard

Report by source cohort:

- Qualified reach and visits.
- Leads or installs.
- Activation and time to value.
- Natural-interval retention.
- Paying conversion, net revenue, refunds, and gross contribution.
- CAC at lead, activated, retained, and paid levels.
- Referral participation and retained referred users.
- Support, quality, and safety guardrails.
- Founder hours per channel.

Avoid combining organic and paid or new and returning users when making allocation decisions.

## Common metric traps

- **Vanity denominator:** quoting users without defining registered, installed, active, retained, or paying.
- **Attributed equals incremental:** assuming every post-click install was caused by the ad.
- **Cheap proxy optimization:** buying low-cost clicks or installs that do not activate.
- **Survivorship:** learning only from visible successes and not the creator's failed products.
- **Channel mixing:** reporting average retention across high- and low-quality sources.
- **Maturity mixing:** comparing a one-day cohort to a three-month cohort.
- **Revenue without contribution:** ignoring fees, refunds, infrastructure, support, and labor.
- **Average without marginal:** scaling while new acquisition becomes progressively worse.
- **Feedback-count fallacy:** treating duplicate feature requests or defects as proof of PMF.
- **Ranking spike:** treating a temporary store or launch leaderboard position as repeatable demand.
- **Waitlist certainty:** treating email entry as payment or retention.
- **Arithmetic drift:** changing the acquisition denominator between spend, clicks, installs, and users.
- **Untracked direct:** assigning missing attribution to brand or word of mouth without evidence.
- **Multiple testing:** selecting a winner from many variants without accounting for false positives.
