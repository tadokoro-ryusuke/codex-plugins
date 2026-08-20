---
name: indie-idea-discovery
description: Research-driven indie product idea discovery, opportunity mining, problem selection, structured ideation, founder-market-fit analysis, and evidence-based idea ranking for apps, SaaS, developer tools, marketplaces, and creator products. Use when the user has no concrete product idea, asks for app or business ideas, wants to find problems worth solving, needs ideas derived from personal experience or a market, wants to expand or compare several early concepts, or needs a shortlist to validate before building. Use $indie-product-marketing after a concrete opportunity has been selected.
---

# Indie Idea Discovery

Discover problems worth solving before proposing products. Combine founder-specific evidence, current market evidence, structured divergence, and independent evaluation. Do not return a generic list of fashionable app ideas.

## Choose the discovery mode

Select the narrowest mode that fits the request:

1. **Founder-first discovery** — inventory the founder's experience, repeated work, access, assets, constraints, and unfair advantages before researching adjacent problems.
2. **Domain-first discovery** — investigate one market, profession, community, workflow, or life situation for unmet needs and weak substitutes.
3. **Friction mining** — analyze reviews, support threads, workarounds, manual processes, spending, and abandoned tasks for opportunity signals.
4. **Concept expansion** — take one seed such as “memo app” or “tool for nurses” and create meaningfully different solution directions.
5. **Portfolio selection** — deduplicate, compare, and rank an existing set of ideas using evidence, hard gates, and founder objectives.
6. **Idea audit** — identify unsupported assumptions, imitation, AI convergence, selection bias, safety risk, and missing validation in an idea-generation method or output.

Infer the mode from context. Ask only for information that would materially change the search space; otherwise state assumptions and proceed.

## Separate evidence from imagination

Classify material statements as:

- **Observed fact** — directly supplied behavior, analytics, spending, workflow, or a verified public fact.
- **Reported fact** — a user, founder, reviewer, or case study reports it without independent verification.
- **Inference** — a conclusion derived from identified evidence and assumptions.
- **Opportunity hypothesis** — a problem, customer, or business claim that still requires a test.
- **Concept** — a possible product response, not evidence that the opportunity exists.
- **Recommendation** — a next action justified by the evidence and uncertainty.

When current market research is requested, browse current sources and cite material claims. Prefer official documents, first-party product and pricing pages, observable customer behavior, raw user research, and peer-reviewed studies. Treat AI summaries, generic idea lists, SEO pages, and unexplained market-size claims as weak inputs.

Read [references/evidence-and-video-audit.md](references/evidence-and-video-audit.md) when using the source video, explaining why combination methods work, assessing AI ideation, or distinguishing interest from demand.

## Phase 1: frame the founder search space

Capture:

- Skills, domain experience, credentials, and communities.
- Repeated daily, weekly, seasonal, and event-triggered behavior.
- Workarounds already built with spreadsheets, scripts, prompts, notes, or manual services.
- Purchases, subscriptions, contractors, and tools used to remove friction.
- People the founder can reach without buying broad attention.
- Proprietary or permissioned data, content, workflows, integrations, or trust.
- Desired customer, business model, sales motion, geography, and language.
- Time, cash, platform, operating, support, and regulatory constraints.
- Revenue objective, desired lifestyle, and work the founder refuses to do.

Do not force every opportunity to originate from the founder. Use founder context to improve judgment, access, and commitment, then verify that other people share the problem.

Use `assets/founder-inventory.md` when the user wants a durable discovery brief. Read [references/discovery-methods.md](references/discovery-methods.md) for interview prompts and behavioral inventory methods.

## Phase 2: mine problems before solutions

Search for evidence of behavior and consequence:

- Repeated complaints tied to a specific situation.
- Manual copying, reconciliation, reminders, approval, scheduling, or reporting.
- Spreadsheets, private scripts, templates, and human services used as substitutes.
- Existing purchases, budgets, contract work, and switching behavior.
- Abandoned tasks, delays, rework, errors, missed revenue, penalties, or emotional cost.
- Product reviews that describe a job, workaround, and failed outcome.
- Support, documentation, community, procurement, and job-posting evidence.
- New technology, regulation, platform, demographic, or cost changes that make a previously weak solution feasible.

Avoid treating feature requests, search volume, large market size, social engagement, or one founder's frustration as sufficient proof. Record the source, date, segment, behavior, and consequence in `assets/problem-evidence-ledger.md`.

Convert each promising signal into a problem statement:

> **[Specific actor]**, when **[triggering situation]**, tries to **[make progress]** but **[friction]**, so they use **[substitute]** and incur **[time, money, risk, or emotional consequence]**.

Reject statements that describe only a feature or demographic.

## Phase 3: generate independently before converging

Run at least three distinct passes:

1. **Founder seed pass** — capture the founder's unaided problems and concepts before showing AI suggestions.
2. **Evidence-led pass** — generate responses only to verified problem cards.
3. **Structured combination pass** — vary explicit dimensions through a morphological matrix.

Add a fourth **unsexy pass** for tedious, operational, regulated, migration, compliance, reconciliation, and service-heavy problems that visually attractive consumer ideas may hide.

Do not generate every pass in one growing conversation where earlier ideas anchor later output. Withhold prior candidates where possible, change the evidence or dimensions intentionally, and merge only after independent passes.

## Use a morphological matrix correctly

Define a problem first, then create rows or columns for dimensions such as:

- Actor or payer.
- Triggering situation and frequency.
- Input and data source.
- Output and user outcome.
- Interaction mode.
- Time, quantity, visibility, or privacy constraint.
- Single-player, collaboration, marketplace, or network structure.
- Automation level.
- Delivery surface and acquisition channel.
- Pricing and payment moment.
- Analogy from another industry.

Generate coherent combinations that improve the user's outcome. Do not perform a full Cartesian product or celebrate novelty without usefulness. Use `assets/morphological-matrix.md` for the working table. Read [references/divergence-and-morphology.md](references/divergence-and-morphology.md) for variation operators, diversity controls, and examples.

## Phase 4: cluster and remove cosmetic variants

Normalize every candidate into:

`customer + trigger + problem + promised outcome + mechanism + payer`

Then:

- Merge ideas that differ only by name, visual style, or AI wording.
- Separate meaningfully different customers, triggers, economics, or mechanisms.
- Mark direct copies, commodity wrappers, and concepts without a distinct wedge.
- Map saturated categories by problem and segment rather than declaring the whole category unusable.
- Preserve a small number of high-variance outliers for evaluation.

Do not let polished mockups outrank stronger problem evidence.

## Phase 5: evaluate with evidence and hard gates

Score candidates only after generation is complete. Evaluate the problem before revealing or rewarding the concept's visual polish.

### Apply hard gates

Do not recommend building when any material gate fails:

- No evidence of a real problem and no ethical way to learn quickly.
- The target customer cannot be reached within the founder's constraints.
- The concept depends on fabricated activity, prohibited data, harmful claims, or unacceptable safety risk.
- The founder cannot deliver the first value or operate the product within the stated time and resources.
- There is no plausible recurring value, payment event, strategic learning value, or intentionally bounded non-commercial objective.

### Compare surviving candidates

Rate each dimension from 0–5 with an evidence grade and uncertainty note:

- Problem evidence, frequency, urgency, and consequence.
- Current spending or costly substitute.
- Reachability and distribution premise.
- Founder insight, access, credibility, and endurance.
- Narrow entry wedge and time to first value.
- Repeat-use or expansion mechanism.
- Payer, pricing logic, margin, and operating burden.
- Technical feasibility and time to learn.
- Competitive differentiation and accumulating advantage.
- Trust, privacy, safety, regulatory, moderation, and platform risk.

Do not hide a hard failure inside a weighted total. Do not use an LLM's confidence or self-score as market evidence. Use the user's objective to break ties rather than inventing universal weights.

Read [references/evaluation-and-handoff.md](references/evaluation-and-handoff.md) for the full rubric, decision rules, and portfolio method. Use `assets/opportunity-card.md` and `assets/idea-portfolio.md` for durable outputs.

## Phase 6: choose learning, not commitment

For each top opportunity, identify:

- The riskiest customer, problem, solution, distribution, retention, and economic assumptions.
- The strongest existing evidence and the most dangerous missing evidence.
- The cheapest ethical action that could disconfirm the thesis.
- A pass, revise, and stop rule chosen before testing.
- The maximum cash and founder hours to spend before review.

Prefer stronger signals:

`content view < click < email < qualified conversation < observed workflow < prototype use < deposit or preorder < repeated use < paid retention`

Treat a mockup, social reaction, ad click, or waitlist as evidence of message interest, not proof of retention or a business.

## Hand off selected opportunities

Stop discovery after producing a decision-ready shortlist. For each selected opportunity, prepare:

- Customer, trigger, job, and consequence.
- Current substitute and evidence.
- Proposed promise and mechanism.
- Founder advantage and reachable channel.
- Recurring value and payer hypothesis.
- Riskiest assumptions.
- First validation and stop rule.
- Evidence ledger and open questions.

Then invoke `$indie-product-marketing` to validate demand, choose channels, prepare launch, instrument metrics, and diagnose growth. Use `assets/validation-handoff.md` for the transfer.

## Produce decision-ready outputs

Return:

1. **Discovery brief** — founder constraints, search boundary, assumptions, and objective.
2. **Evidence map** — observed facts, reported facts, inferences, gaps, and source quality.
3. **Problem landscape** — clustered problem statements and rejected false signals.
4. **Divergence record** — independent passes, matrix dimensions, and duplicate controls.
5. **Opportunity portfolio** — normalized concepts with hard gates, scores, confidence, and tradeoffs.
6. **Top opportunity cards** — normally three, unless evidence supports fewer.
7. **Validation queue** — riskiest assumption, test, budget, duration, and decision rule for each finalist.
8. **Recommendation** — pursue, research further, park, or reject, with reasons.

Return fewer ideas with stronger evidence instead of padding the list. If the research finds no credible opportunity, say so and recommend the next discovery surface rather than inventing confidence.
