# Reference patterns and transfer decisions

Use these dated observations to generate design hypotheses. Revisit the live page before describing its current design. Preserve the difference between visible marketing material, observed interaction, and working product behavior. No conversion analytics or commercial outcomes were available for this research.

## SPREAD: make a complex mechanism legible

Source: [SPREAD](https://www.spread.ai/), observed 2026-09-08 through public page text and desktop browser screenshots.

**Observed:** An outcome-led hero on a pale technical grid uses orange accents, fine rules, and small engineering-style labels. A large product diagram follows the headline. Requirements, product relationships, and error investigation structure the explanation. A later requirements example pairs a document with linked analysis. The page offers a guided evaluation and includes customer material and objections.

**Mechanism hypothesis:** Consistent engineering cues can make the page and product feel related; connecting analysis to source material can explain why a visitor should inspect an AI result.

**Transfer:** Borrow readable relationships and evidence near results for products whose users must understand causality. Simplify to a single useful example for a smaller product. Do not inherit an enterprise sales motion, technical density, badges, or claims merely because the composition is attractive.

**Limit:** Desktop presentation was inspected; mobile behavior, product execution, accuracy, and conversion effects were not verified.

## Circleback: connect an immediate promise to visible output

Source: [Circleback](https://circleback.ai/), observed 2026-09-08 through public page text and desktop browser screenshots.

**Observed:** A centered headline promises meeting-note quality above a short explanation and orange pill CTA on a pale blue background. A large meeting example shows notes and assigned actions. Feature sections cover notes, actions, automation, search, and transcription. Testimonials, integration material, and security claims address trust. The logo wording refers to people at companies, a narrower claim than organization-wide adoption.

**Mechanism hypothesis:** A familiar job and recognizable output can reduce explanation before trial. Placing relevant proof after the initial example can answer doubts without crowding the hero.

**Transfer:** Pair one concrete promise with a readable result and a fitting primary action. Bring forward the output the visitor wants. Use only evidence the new product actually has; a prototype cannot inherit a live product's trial or social proof.

**Limit:** Trial completion, integrations, security claims, mobile behavior, and conversion performance were not independently verified.

## Inkdrop: show use and make the maker discoverable

Source: [Inkdrop](https://www.inkdrop.app/), observed 2026-09-07 through public browser inspection recorded during the Stride LP study.

**Observed:** Concise value copy, a large editor demo in a desk setting, concrete feature examples, pricing and FAQ, and paths to the maker, blog, and community.

**Transfer hypothesis:** Let visitors picture using the product and inspect its development history. Use an authentic maker presence when available. Create original examples and photography; do not copy the editor's assets or assume maker visibility caused sales.

Process reference: Takuya Matsuyama's [Inkdrop design account](https://www.devas.life/how-i-designed-my-saas-landing-page-with-ai-tools/), published 2026-09-07; public article text read in-browser on 2026-09-09. Treat tool preferences as personal experience, not benchmarking or conversion evidence.

## Granola: organize around a recognizable work situation

Source: [Granola](https://www.granola.ai/), observed 2026-09-07 through public browser inspection recorded during the Stride LP study.

**Observed:** Large typography addresses a busy meeting context; note visuals and a before/during/after story carry the explanation.

**Transfer hypothesis:** Align the headline, example, and section sequence around the same recurring situation. Choose typography, colors, and image treatment from the new product's brand rather than copying this reference's surface style.

## Things: establish the category and let the product breathe

Source: [Things](https://culturedcode.com/things/), observed 2026-09-07 through public browser inspection recorded during the Stride LP study.

**Observed:** A product icon, clear personal task-manager category, introduction-video path, ample whitespace, and product screens.

**Transfer hypothesis:** Give a first-time visitor enough category information to interpret the product example. Use whitespace to prioritize that example. Do not borrow awards, availability, or download promises from a mature product for an unreleased one.

## Mobbin and UI Pocket: compare section roles

Sources, observed 2026-09-07:

- [Mobbin Sites](https://mobbin.com/discover/sites/latest): the public latest view exposed four previews and section categories such as hero, pricing, and explanation; further material was marked Pro.
- [UI Pocket Sites](https://www.ui-pocket.com/site): the public view exposed six company-site previews and required login for more. Browser inspection succeeded despite failed text retrieval.

**Transfer hypothesis:** Compare how a section introduces a promise, illustrates a workflow, or resolves an objection. Record the actual sample and viewing limits. Gallery inclusion is a discovery aid, not evidence of conversion success or a country's uniform aesthetic. Do not imply that an entire catalog or gated detail page was inspected.

## Stride: preserve the mechanism while changing the language

Case source: the local Stride study and English/Japanese landing-page prototype, recorded 2026-09-07. The study lived at `stride/docs/research/2026-09-07-global-lp-design.md`; the lessons below are self-contained and do not require that repository to be installed.

**Context:** A prelaunch desktop productivity product connected a meeting to project context and the next task. The available LP interaction was an illustrative demo, not the complete recording or AI pipeline.

**Applied direction:** Use a headline about resuming work after meetings, followed by a three-state meeting/context/next-action example. Let a visitor inspect a result's source and download a synthetic Markdown artifact. Repeat selected brand cues between the page and the example while giving the marketing copy more room than the product UI.

**Readiness decision:** Make the demo the primary action. Explain the development stage and unavailable registration instead of returning a fake signup success. A later working registration flow would enable a separate demand experiment. Keep ownership of Markdown distinct from whether cloud processing is involved.

**Localization decision:** Adapt the headline naturally and translate demo content, source dialogs, FAQ, accessible names, and downloadable samples. Share behavior and styling; adjust CJK typography and narrow navigation. Keep proposed dollar pricing as a proposal rather than inventing a yen offer.

**Recorded verification, not rerun for this skill:** The prototype study reports checks of both languages at widths 320, 375, 768, 1024, and 1440 pixels, demo tabs, dialogs, Escape/focus restoration, FAQ, and language switching. Those observations do not establish Safari/Firefox behavior, screen-reader accessibility, registration delivery, or demand.

**Generalize the reasoning, not the brand:** White/ink/orange, restrained borders, and a static HTML implementation fit that project's existing constraints. They are not requirements for future LPs. A colorful page, editorial photography, a serif headline, or an existing React stack can satisfy the same visitor questions.
