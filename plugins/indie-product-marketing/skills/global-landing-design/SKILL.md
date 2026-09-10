---
name: global-landing-design
description: "Global landing page design: research reference sites, design or build product landing pages for international audiences, and adapt an existing LP across languages. Use for English-language SaaS or indie product LPs, reference-based visual direction, product demos, and landing-page localization or review."
---

# Global Landing Design

Turn product context and reference-site observations into a coherent landing page that helps a particular visitor understand, trust, and try the product. Treat visual choices as hypotheses until measured with the intended audience.

## Choose the requested scope

- **Research:** inspect references, explain mechanisms and tradeoffs, and propose a direction. Stop before implementation if the user asked for research only.
- **Design or build:** use the research to produce the requested wireframe, copy, or working page. Continue through proportional verification.
- **Localize or review:** preserve the accepted concept and inspect the requested languages or problems. Do not restart brand discovery for a small edit.

Use this workflow for landing pages. Handle a one-sentence translation directly; do not turn an unrelated product-dashboard request into a marketing-page project.

## 1. Ground the brief

Read the product brief, current page, repository instructions, and design system before editing. Identify:

- Audience, language, buying context, and likely traffic source.
- The recurring situation or job, the promised outcome, and the product category.
- Buying motion: self-service, guided evaluation, purchase, or prelaunch interest.
- Primary next action and what actually works today: demo, trial, download, booking, payment, or registration.
- Available evidence: real screens, sample outputs, named customer permission, product availability, and constraints on claims.
- Existing brand, stack, localization structure, and files in scope.

Use existing evidence first. Record material assumptions and proceed with reversible work when information is missing. Ask only questions that affect the result materially; do not require interviews before a web-only experiment. For a substantial page, copy [the brief template](assets/lp-brief.md) into the target project's normal documentation location and keep decisions and verification there.

Define a message spine: **visitor situation → promised outcome → visible mechanism → available next step**. Keep category and platform legible if an evocative headline alone would be ambiguous.

## 2. Inspect references for mechanisms

Prioritize user-supplied URLs. Inspect the current rendered page when visual claims matter; use page text for copy and section structure. Aim for a few relevant references, not an exhaustive inspiration collection. Compare a close product-category reference with a reference that solves a different communication problem.

Read [reference patterns](references/reference-patterns.md) for dated observations of SPREAD, Circleback, Inkdrop, Granola, Things, Mobbin, UI Pocket, and the Stride prototype. Use these as starting points, not current facts about a redesigned site.

For each relevant reference, record:

| Observed, with URL and date | Communication mechanism hypothesis | Adopt, adapt, or reject for this product |
| --- | --- | --- |
| Describe visible copy, layout, demo, or interaction. | Explain the visitor question it may resolve. | Tie the decision to audience, readiness, and brand. |

Record viewport and access limits. Distinguish screenshots, observed interactions, marketing claims, and measured outcomes. If rendering or access fails, label text-only findings and continue with accessible sources; do not invent visuals or imply a paid gallery was fully inspected. Do not infer conversion performance from polish, logos, awards, or directory inclusion.

Extract relationships such as promise-to-demo continuity, proof placement, and information density. Create original copy and assets; do not reproduce another company's branding, customer endorsements, or proprietary screens as the new product's own.

## 3. Choose a page argument

Use the buying-motion and evidence tables in [the design playbook](references/design-playbook.md) when deciding section order and proof.

Propose one coherent direction by default. Explain why its tone, composition, and product presentation fit this audience. Offer alternatives only when they represent an unresolved decision or the user requests them.

Map sections to visitor questions, not a fixed section quota:

1. **Is this for me?** A specific outcome, enough category/context, and a primary action.
2. **What will I do or receive?** A substantial, readable product example early in the page.
3. **How does it fit my work?** A small number of concrete situations or steps.
4. **Why believe it?** Evidence proportional to product maturity, near the claim it supports.
5. **What would stop me?** Relevant questions about price, setup, compatibility, data, or availability.
6. **What happens next?** Repeat the available primary action after useful context.

Reorder or omit sections when the buying context warrants it. Keep a secondary action subordinate rather than making every button equally prominent. Match labels to actual behavior: a local prototype preview is not a live trial, and an informational dialog is not a completed signup.

## 4. Establish the visual grammar

Preserve accepted brand rules. Define the relationship between marketing typography, product-UI density, whitespace, surfaces, imagery, and CTA emphasis before styling isolated sections.

Judge exploratory AI sketches by product comprehension, distinctiveness, and maintenance cost; record why a direction was rejected. For product-based demos, follow the staged workflow in [the design playbook](references/design-playbook.md#iterate-a-product-based-demo).

- Give the first viewport a clear focal point and readable hierarchy. Let a large demo remain comprehensible rather than shrinking an entire dashboard into decorative noise.
- Use product-specific visual material: a document, timeline, artifact, device context, or task flow that supports the promise.
- Carry a few intentional brand cues across the page and demo. Use section contrast or layout changes when they help the argument progress.
- Choose fonts, photography, gradients, illustration, grids, rounded corners, and motion for the product and audience. Do not hard-code a single orange/white indie aesthetic or claim that a nationality has one design preference.
- Make mobile composition deliberate: simplify dense examples, preserve reading order, and keep primary actions and language links accessible. Prefer a clearly labeled excerpt to unreadable miniaturization.
- Keep motion purposeful, controllable where applicable, and compatible with reduced-motion preferences. Avoid requiring animation to understand the message.

## 5. Make product proof honest and useful

Show an understandable **input → transformation → result → next action** when it suits the product. For AI-derived results, make source relationships visible where they are part of the product's trust promise; do not invent accuracy, confidence scores, integrations, or provenance that the product cannot provide.

Use real, permission-safe product examples when available. Otherwise label illustrative data and distinguish a prototype interaction from a released capability. An early product can demonstrate a real sample artifact or a narrow working flow without manufacturing reviews, customer logos, or usage counts.

Place material qualifications next to affected claims. Local file ownership does not establish fully offline processing; proposed prices and target platforms are not released terms. Preserve the narrower meaning of endorsements, such as individual users at a company versus company-wide adoption.

## 6. Build or localize within the existing project

Use the current stack, file structure, design tokens, and accessible components. Choose a simple standalone prototype only when that suits the task. Do not require a particular framework, hosting provider, analytics service, or external font just to apply this skill.

Connect promised interactions to their actual destinations. Keep demos, download artifacts, metadata, and visible copy consistent. If a submission backend is unavailable, offer a truthful available action and make the prototype state clear; never show successful registration without submission. Use synthetic or authorized data in public examples.

For localization:

- Adapt the outcome and examples into natural language while preserving product facts and maturity.
- Translate navigation, accessible names, dialogs, form states, FAQ, demo content, downloads, and relevant metadata as well as headings.
- Recheck line breaks, CJK tracking and line height, long words, narrow navigation, and language switching. Support RTL layout when a target language requires it.
- Preserve approved pricing and currency; do not invent regional offers, dates, or capabilities through translation.
- Reuse structure and behavior where appropriate. Follow the project's locale routing and SEO conventions; do not expose an unpublished prototype to indexing accidentally.

## 7. Verify and hand back evidence

Run the project's applicable checks and inspect the final rendered result. For a working page, verify desktop and mobile layouts, including the narrowest supported width, localized long text, navigation, and the promised main action. Verify keyboard access and focus behavior for interactive components; check reduced motion if motion was added. Record what actually ran and which browsers, devices, accessibility checks, and integrations remain untested.

Keep three conclusions separate:

- **Design review:** how well the page expresses the intended product and audience.
- **Implementation verification:** which layouts, interactions, and checks were observed working.
- **Demand evidence:** what real visitors, submissions, qualified trials, or purchases demonstrated.

For a demand experiment, define one primary outcome, its denominator, traffic source, language, and an observation window. Count an actual submission as a submission, not a CTA click. Treat gallery feedback and Product Hunt engagement as distribution or interest signals until downstream behavior is measured. Use `$indie-product-marketing` when a broader acquisition or launch plan is requested.

Hand back the artifact, major reference-to-design decisions, verification evidence, and the next unresolved product or measurement decision. Link the relevant files and sources. Do not claim deployment, model accuracy, demand, or conversion improvements from a local demo.

Use [evaluation cases](references/evaluation-cases.md) when testing changes to this skill. Judge resulting behavior and artifacts; keyword presence and packaging validators alone do not establish successful skill execution.
