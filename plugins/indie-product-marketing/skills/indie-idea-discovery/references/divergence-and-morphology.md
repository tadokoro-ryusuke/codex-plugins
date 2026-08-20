# Divergence and Morphological Ideation

Use this reference after credible problem cards exist or when expanding a concrete seed into meaningfully different directions.

## Contents

1. Stage the process
2. Run independent passes
3. Build a morphological matrix
4. Apply variation operators
5. Protect diversity in AI-assisted work
6. Cluster and normalize
7. Worked example

## 1. Stage the process

Keep four activities separate:

1. **Discover** — collect founder context and customer-problem evidence.
2. **Diverge** — produce different problem framings and solution mechanisms.
3. **Converge** — remove duplicates, apply gates, and compare tradeoffs.
4. **Validate** — expose risky assumptions to behavior and economic commitment.

Do not alternate between creating and scoring every individual idea. Immediate evaluation anchors later generation and rewards concepts that are easy to explain rather than opportunities with stronger evidence.

## 2. Run independent passes

Generate from multiple perspectives before merging results.

### Pass A: founder seed

Capture the founder's unaided observations and ideas first. Ask what they noticed, built privately, paid for, or repeatedly explained. Preserve the original wording.

### Pass B: evidence-led

Give the generator only problem cards and source evidence. Ask for several mechanisms that change the customer's outcome, including software, service, workflow, integration, and “do nothing differently” alternatives.

### Pass C: morphological combinations

Define dimensions and alternatives, then sample coherent configurations. Require each configuration to state why the elements reinforce one another.

### Pass D: unsexy opportunities

Search explicitly for:

- Reconciliation and exception handling.
- Approvals, audits, evidence collection, and compliance.
- Data migration, cleanup, mapping, and handoff.
- Scheduling, follow-up, reminders, and renewal.
- Internal reporting and customer reporting.
- Service enablement and human-in-the-loop operations.
- Failure recovery, monitoring, and maintenance.
- Accessibility, localization, permissions, and privacy.

### Optional pass E: adversarial reframing

Ask how the problem disappears through policy, training, a marketplace, an incumbent feature, a platform change, or a cheaper service. This produces alternatives and disconfirming paths, not only products.

## 3. Build a morphological matrix

Choose dimensions that materially change customer value or business behavior. A typical matrix includes:

| Dimension | Example alternatives |
|---|---|
| Actor | Individual, team lead, operator, advisor, administrator |
| Trigger | Scheduled deadline, exception, handoff, life event, threshold crossed |
| Input | Manual entry, import, sensor, document, message, existing system event |
| Primary progress | Decide, remember, reconcile, coordinate, prove, create, recover |
| Mechanism | Checklist, automation, copilot, concierge, marketplace, integration |
| Interaction | Ambient, batch, conversational, visual, approval queue, API |
| Constraint | Private, offline, low-literacy, regulated, time-critical, shared device |
| Output | Decision, notification, artifact, transfer, audit trail, completed service |
| Payer | User, employer, client, partner, institution, transaction participant |
| Acquisition | Existing community, search intent, integration, partner, outbound, referral |
| Recurrence | Daily, weekly, event-triggered, renewal, project-based, one-time migration |
| Advantage | Workflow depth, data improvement, trust, integration, distribution, service |

Do not fill every cell mechanically. Remove irrelevant dimensions and add domain-specific ones. For healthcare, privacy, clinical responsibility, and workflow ownership may dominate. For marketplaces, supply, trust, liquidity, and dispute handling may dominate.

### Select combinations

For each problem card:

1. Fix the actor, trigger, and desired progress unless testing a deliberate reframe.
2. Pick alternatives from three to six remaining dimensions.
3. Reject incompatible or ethically unacceptable combinations immediately.
4. Explain the causal chain from mechanism to outcome.
5. State who changes behavior and who pays.
6. Record which assumption is novel rather than calling the whole idea novel.

Generate a representative sample, not the Cartesian product.

## 4. Apply variation operators

Use operators when candidates remain too similar:

- **Remove** — eliminate a step, decision, input, account, meeting, or screen.
- **Constrain** — design for one role, one event, one output, or one severe boundary.
- **Invert** — push instead of pull, prevent instead of repair, buyer becomes seller, private becomes shared with permission.
- **Transfer** — adapt a mechanism from another industry while preserving the problem logic.
- **Unbundle** — isolate the highest-consequence step from a broad suite.
- **Bundle around progress** — combine fragmented tools needed for one end-to-end job.
- **Automate selectively** — automate stable steps and keep judgment or exception handling human.
- **Productize a service** — standardize intake, evidence, delivery, and feedback before automating.
- **Service-enable software** — use software to make a trusted human service faster or more consistent.
- **Change the payer** — find the party that benefits economically from the outcome.
- **Change the moment** — intervene before, during, or after the triggering event.
- **Change the commitment** — free diagnostic, paid setup, subscription, transaction, outcome-based, or licensed workflow.
- **Make failure visible** — monitoring, evidence, escalation, recovery, and auditability.
- **Use non-consumption** — make a previously inaccessible task affordable or operable.

Every operator must preserve or improve the customer's desired progress. Novelty without causality is noise.

## 5. Protect diversity in AI-assisted work

### Preserve independent input

- Write founder seeds before displaying model suggestions.
- Use separate prompts or contexts for different passes.
- Give each pass a different evidence packet or transformation objective.
- Request contrasting mechanisms, not “ten more ideas.”
- Include non-software and incumbent-improvement alternatives.

### Avoid synthetic evidence

Ask the model to label assumptions and missing sources. Never let it fabricate interview quotes, review excerpts, customer counts, willingness to pay, or competitor facts.

### Delay model evaluation

Do not show model-generated ratings during divergence. When converging, ground each rating in the evidence ledger. Treat the model as an organizer and critic, not a market participant.

### Use prompt roles carefully

Useful roles specify a lens, not fake authority:

- “Generate mechanisms as a workflow designer optimizing handoffs.”
- “Generate alternatives as a service operator handling exceptions.”
- “Find privacy-first mechanisms that minimize retained data.”
- “Challenge whether software is necessary.”

Avoid prompts that impersonate customers or ask for certainty without evidence.

## 6. Cluster and normalize

Normalize every candidate into:

`actor + trigger + problem + promised outcome + mechanism + payer`

Then compare:

- **Cosmetic duplicate:** same actor, trigger, problem, outcome, and mechanism; only name, style, or AI phrasing differs.
- **Feature variant:** same opportunity, different implementation detail. Keep under one concept unless it changes adoption or economics.
- **Segment variant:** different actor or payer with meaningfully different reach, workflow, or risk. Preserve separately.
- **Mechanism variant:** same problem, materially different delivery or operating model. Preserve for evaluation.
- **Problem reframe:** different desired progress or consequence. Return it to discovery for evidence review.

Keep one representative candidate per cosmetic cluster and record discarded variants. Preserve one or two high-variance outliers if they are coherent, even when evidence is incomplete.

## 7. Worked example

Territory: Japanese households managing recurring administrative obligations.

Problem card:

> A household organizer, when a government, school, insurance, or property notice arrives, tries to identify and complete the required action but deadlines and required documents are scattered across paper and messages, so they use piles, calendar entries, and family chat and risk late or duplicated action.

Possible dimensions:

- Input: camera capture, forwarded email, manual selection, partner message.
- Mechanism: private extraction, shared checklist, concierge review, calendar integration.
- Constraint: sensitive documents, mixed digital literacy, shared responsibility, Japanese forms.
- Output: next-action card, evidence checklist, delegated task, completion record.
- Payer: household, employer benefit, property manager, insurer, local service partner.

Coherent configurations:

1. Private on-device notice extraction → next-action card → household subscription.
2. Human-reviewed intake → evidence checklist for complex life events → per-case payment.
3. Property-manager message integration → tenant action and completion trail → property manager pays.

These are not validated opportunities. They are mechanism and payer variants derived from one problem. Next compare reachability, data risk, consequence, current substitutes, and evidence before choosing a test.
