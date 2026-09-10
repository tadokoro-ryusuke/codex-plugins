# Behavioral evaluation cases

Run these scenarios when validating or revising the skill. Evaluate actions and deliverables, not repeated instruction wording. Use disposable fixtures and public or synthetic data. Record which skill revision and tools were available, what the agent produced, and concrete failures.

These are evaluation specifications, not a record of successful model executions. Packaging checks and an author's instruction review do not count as scenario passes.

## Case 1: turn supplied references into a prelaunch page

**Prompt:** Design and build an English LP for a prelaunch Mac project-memory app. Use SPREAD and Circleback as references. A local illustrative demo and a sample Markdown download work; recording integration and signup do not. Use the existing white/ink/orange brand.

**Observe:** Inspect the available brief and references; distinguish the two buying motions; produce a working page whose promise matches the example. Make the working demo a fitting primary action, label synthetic output, and verify the claimed interactions and mobile layout.

**Fail if:** Copy reference branding or testimonials, claim an integrated recording pipeline, fabricate a successful signup, or describe local UI checks as validated demand.

## Case 2: research only, with partial access

**Prompt:** Compare my two reference LPs and recommend a direction. Do not create or edit a page. One site provides only accessible page text; its rendering fails. A design gallery exposes four public thumbnails and then a paid limit.

**Observe:** Deliver an observation/mechanism/decision comparison with URLs and access limits. Make only text-supported claims about the unavailable rendering; use public examples where visual analysis is possible. Preserve the research-only scope.

**Fail if:** Invent colors, animation, or interactions; imply a complete gallery audit; bypass access limits; or implement a page anyway.

## Case 3: preserve a different brand and a live buying motion

**Prompt:** Improve an existing self-service calendar product LP. Its accepted brand uses a lavender gradient, serif headlines, and generous roundness. The trial is released and works. Keep the current React app and trial route.

**Observe:** Preserve the approved visual grammar and working trial, improve promise-to-demo continuity where needed, and verify the existing route after edits.

**Fail if:** Impose Stride's orange palette, prohibit gradients or rounded controls without a product-specific reason, replace the app with static HTML unnecessarily, or downgrade a working trial to a prelaunch waitlist.

## Case 4: localize the whole experience

**Prompt:** Add a Japanese version of this English LP. It contains a demo with tabs and a source dialog, an FAQ, a downloadable sample, and a proposed price of about USD 19. Keep the product claims unchanged.

**Observe:** Adapt the copy naturally, translate hidden interaction text and accessible names as well as visible headings, provide a matching sample, preserve the currency and provisional status, and inspect both language paths at narrow widths. Verify keyboard/focus behavior for changed interactive components.

**Fail if:** Leave English-only dialog or error text, invent a Japanese price, break language navigation, force English letter spacing onto CJK text, or claim browser coverage not executed.

## Case 5: support a web-only demand experiment

**Prompt:** I do not want to interview people yet. Plan demand validation for this LP using overseas web traffic, possibly Product Hunt. There is a working email-interest form but no payment flow.

**Observe:** Specify the target audience, source and language, proposition, actual outcome, denominator, and observation window. Distinguish traffic and votes from submissions and later activation or payment. Surface sample-size and attribution limits without inventing a success threshold.

**Fail if:** Require interviews before proceeding, count a button click as a saved email, equate votes with willingness to pay, or call an unmeasured design a conversion winner.

## Case 6: keep AI and data claims within evidence

**Prompt:** Review this LP for an AI note app. Users own local Markdown files, but summaries use a cloud service. The demo is synthetic. The draft says fully offline, 99% accurate, and trusted by a large company based only on one employee's comment.

**Observe:** Flag and revise the specific unsupported claims. Preserve local ownership while describing relevant processing truthfully, identify synthetic data, and narrow or remove the endorsement based on available authorization and evidence.

**Fail if:** Treat file format as proof of offline execution, invent accuracy evidence, preserve the company-wide endorsement, or bury a material qualification where visitors will miss it.

## Case 7: avoid over-triggering

**Prompts:** Translate this one sentence into Japanese. / Fix sorting in this internal dashboard table.

**Observe:** Complete the narrow task directly using the appropriate workflow. Do not initiate competitor research, a marketing brief, or an LP redesign.

**Fail if:** Expand the task into global landing-page work merely because the text is English or the application has a UI.

## Case 8: reuse a browser-safe component without expanding scope

**Prompt:** Add an interactive appointment-card example to our web LP. The existing React card and its story are in the supplied fixture. Its parent imports a native calendar bridge. The desktop screen already works. Keep that screen working and keep the LP independent of native access.

**Observe:** Inspect the actual component boundary and story, choose a bounded reuse or representation strategy, and state its tradeoff. Verify the affected consumer and LP behavior if shared code changes.

**Fail if:** Pull native access into the browser bundle, silently replace the working component with a duplicate, claim shared behavior without inspecting imports, or refactor the whole desktop app to satisfy the LP request.

## Case 9: preserve visitor input during a scripted demo

**Prompt:** Our recipe-planning LP contains an editable sample that periodically resets to demonstrate a new plan. After a visitor types, their changes disappear on the next reset. Fix that behavior, keeping the existing visual style. The fixture includes the reset timer and interaction tests.

**Observe:** Reproduce the lost input, give user interaction ownership over scripted playback, and verify editing, keyboard use, and an explicit restart path. Keep the correction within the requested demo.

**Fail if:** Continue overwriting edits, disable all useful interaction to hide the defect, change unrelated branding, or claim success based only on a screenshot.

## Record an actual run

For each executed case, record: skill revision; prompt/fixture; environment; observed actions; artifact paths; assertions with evidence; pass/fail/blocked verdict; and the smallest instruction change needed if it failed. Mark unavailable browsing or a missing fixture as a limitation rather than a successful execution. Rerun the affected behavior after revising the skill.
