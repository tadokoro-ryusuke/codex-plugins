# Design playbook

Use the tables as decision aids, not universal conversion rules. Select what fits the current brief and evidence.

## Match the buying motion

| Context | Visitor needs to understand | Useful early proof | Primary action when available |
| --- | --- | --- | --- |
| Self-service product with a working trial | The immediate job, useful output, and setup effort | One recognizable workflow or real output | Start the trial or use the product |
| Complex product with guided evaluation | Fit to their workflow, mechanism, and evaluation scope | A concrete case, linked evidence, or realistic walkthrough | Book a clearly described evaluation |
| Indie product available for purchase | The experience, ownership, terms, and ongoing support | Product use, actual artifacts, maker or release history | Buy, download, or start an available trial |
| Prelaunch product or prototype | The intended outcome and what can be experienced now | A labeled demo, sample artifact, or narrow working feature | Try the demo; register interest only if submission works |

Do not force a sales meeting onto a low-friction product or a nonexistent trial onto a complex prototype. Prefer a primary action that advances the visitor's decision over one that merely sounds impressive.

## Build the argument before the section inventory

Write a sentence that connects the visitor's situation, the improvement, and the mechanism. Then choose the smallest sequence that makes it believable.

For example, for a fictional project-memory app: a visitor returning to a client project sees what changed, why it changed, and the next action. A useful example is a short meeting excerpt becoming a project update with a source link. A collage of unrelated dashboards would leave the central claim unexplained.

Keep headline and demo about the same outcome. If the promise is easier project resumption, do not spend the first screen demonstrating only transcript accuracy. If the promise is reliable engineering analysis, a traceable relationship may matter more than a friendly note preview.

Use feature sections to explain distinct situations, outputs, or objections. Merge repeated claims that only reword the headline. Keep a section when it helps a visitor make a decision; do not add a pricing table, logo wall, or FAQ merely to meet a template.

## Choose the proof the product can support

| Product evidence available | Show | Avoid inventing |
| --- | --- | --- |
| Concept or mockup | Clearly labeled example and present limitations | Released functionality, integrations, customer adoption |
| Narrow working capability | Actual flow and output, with its boundary | A fully integrated workflow that the demo only simulates |
| Released product, limited customer evidence | Real screens, documentation, terms, changelog, maker identity | Testimonials, counts, and numerical improvements |
| Authorized customer evidence | Attributed use case and the precise claim supported | Broader company adoption or causal metrics not established by the evidence |
| Measured product outcome | Measurement context, population, period, and limitation | An unexplained percentage detached from its baseline |

Put proof near the corresponding claim. Keep a synthetic label visible where the example is first interpreted, rather than hiding it only in a footer. Describe product security and data processing using verified product facts; decorative badges do not substitute for them.

## Compose a coherent visual direction

Decide these relationships together:

| Decision | Question | Example tradeoff |
| --- | --- | --- |
| Tone | Should the experience feel technical, calm, expressive, editorial, or playful for this job? | A technical grid may explain system relationships but can overcomplicate a simple note app. |
| Hierarchy | What should be read first, and what supports it? | A large headline needs a restrained nearby paragraph and an unmistakable action. |
| Product scale | What part of the product remains understandable at this size? | A cropped workflow can communicate more than an entire dashboard scaled down. |
| Image language | Does the visual reveal use, outcome, context, or merely decorate? | A desk photo can locate the product in daily work; a diagram can reveal relationships. |
| Continuity | Which cues connect the marketing page to the actual product? | Reuse type roles, colors, and source indicators while allowing different density. |
| Rhythm | Where does the visitor need a new focus? | Alternate a large example with a short explanatory section, rather than repeating identical feature cards. |
| Motion | What change does animation help explain? | Animate a transformation only if the start and end states also make sense without motion. |

Use a small intentional token set rather than many unrelated effects. Choose contrast, readable type, and touch targets suitable for the current design system. Do not turn a reference's exact color, radius, font, or maximum line length into a global rule.

## Design the example as a short experience

Use enough realistic content to support a meaningful decision, while removing sensitive data and irrelevant density.

1. **Entry:** show the input or recognizable starting situation.
2. **Change:** expose one transformation or useful interaction.
3. **Result:** show the artifact at a readable scale.
4. **Continuation:** make the next action or destination understandable.

Distinguish a video, clickable mockup, real interactive feature, and live trial in both labeling and behavior. If tabs are merely illustrative states, do not describe them as executing the backend. Provide static alternatives when needed; video or motion should not be the only way to understand the outcome.

For downloadable artifacts, align filename, language, contents, and source labels with the promise. For registration, verify actual request and error states when connected. If the backend is outside scope, expose an honest demo or availability state without pretending a contact was saved.

## Iterate a product-based demo

Begin with a static frame; inspect it before adding one working interaction, then optional motion. For reusable UI, point to existing component files, realistic stories, and documentation. Review and verify each extraction separately. Keep the current phase and next action in the project brief. Report device/browser, observed symptom, and suspected cause separately when diagnosing defects.

Apply these engineering checks when adapting that workflow to a project:

- Before sharing a component, inspect its browser compatibility, native imports, persistence, authentication, bundle cost, and coupling to application state. Keep demo fixtures or adapters separate from production integrations. If separation is disproportionate, document a smaller representation; do not make an application-wide refactor an implicit prerequisite for LP work.
- Assign ownership of input state in a replaying demo. On user interaction, stop competing scripted changes and preserve user edits; make restarting an explicit action. Check focus, scrolling, interrupted playback, and a reduced-motion path. A passing animation preview does not verify these states.
- Check the demo and original consuming screen after a shared-component change. Inspect the resulting CSS and state logic for duplicate implementations or compensation for an unexplained layout bug. Prefer fixing the responsible layer over stacking unrelated overrides.

Use these checks only when their corresponding behavior is in scope. A static example need not gain autoplay, a shared package, or a new test framework.

## Adapt the page across languages

Keep the message and product facts stable while adapting expression. Avoid mechanically preserving English line breaks or letter spacing in Japanese. Keep platform names, terms, and prices consistent with approved product decisions.

Audit the whole experience: browser title and description, navigation, demo records, labels for assistive technology, forms and errors, dialogs, FAQ, downloads, and the return path to another language. For multilingual public pages, follow existing canonical and language-alternate conventions and verify route targets. For an unpublished local prototype, preserve its current indexing boundary.

Inspect the smallest supported viewport and a realistic long-text state in each target language. Prefer stacking, selective cropping, or a simpler example over illegible miniature UI. Keep primary actions and locale controls reachable. Check bidirectional layout and mixed numbers/labels when supporting RTL languages.

## Separate review from learning about demand

Record evidence at its actual level:

| Evidence | What it supports | What it does not establish |
| --- | --- | --- |
| Source and rendering review | Intended message, visual hierarchy, and visible limitations | Visitor comprehension or conversion improvement |
| Working local interaction | The specific observed UI flow | Delivery of real email, production availability, or AI quality |
| Real traffic and events | Observed behavior for a source, locale, and period | General market demand or willingness to pay from clicks alone |
| Verified trial, activation, or purchase | A stronger downstream outcome | Retention or profitable acquisition without further evidence |

For a web-only validation request, define a small traffic experiment around one proposition and one real outcome. Capture traffic source and language, the denominator, observation period, and downstream result. Keep demo engagement, submitted interest, confirmed interest, activation, and purchase distinct. State insufficient evidence when samples are small or mixed; do not invent a universal CVR threshold or require interviews as a prerequisite.

When changing an existing page, identify what behavior the change is meant to improve before proposing an A/B test. Use the project's actual traffic and measurement capabilities to decide whether an experiment is feasible. Do not label a visual refresh a growth result before observing visitor behavior.
