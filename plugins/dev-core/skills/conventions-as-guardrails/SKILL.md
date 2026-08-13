---
name: conventions-as-guardrails
description: "Translate coding, naming, and logging conventions into forms an AI agent can follow deterministically: formatter/linter configs, strict typing, architecture tests, CI gates, and agent hooks — leaving docs with only un-toolable intent and an explicit NG list. Reference skill loaded by dev-core workflow skills; invoke explicitly with $conventions-as-guardrails when bootstrapping a new repo, building a project starter kit, writing or trimming AGENTS.md, configuring lint/CI/hooks, defining a naming table or structured-logging standard, or when conventions exist on paper but keep getting violated."
---

# Conventions as Guardrails — enforce conventions with tooling

**Iron rule: every enforceable convention goes into tooling. Documents keep only intent that cannot be tooled, plus an explicit NG list.**

Why: an AI agent follows natural-language conventions (AGENTS.md) only probabilistically. Deterministic checks — lint, types, tests, hooks — are the only ones that reproduce 100% of the time.

The development principles themselves (TDD / SOLID / architecture / security) live in $best-practices. This skill owns the process of translating those principles into unbreakable form.

## Division of labor: what the AI does vs. what only humans can decide

Before running this skill, review this split. Everything in the right column must be confirmed with a human before it is finalized.

| The AI (executor of this skill) does | Only humans can decide |
|---|---|
| Translate conventions into tool configs (generate linter, formatter, architecture-test, hook settings) | Which style guide is the standard (selection of the convention itself) |
| Draft diffs against an off-the-shelf style guide; draft config files | Ubiquitous-language definitions (agreed with the customer) |
| Auto-generate dependency graphs; turn dependency rules into tests | Layer count and abstraction level (depends on project size and maintenance contract) |
| Draft the naming table and the logging-convention table | Approval of any new disable comment |
| Detect violations, apply mechanical fixes, wire checks into CI | Log retention periods and audit requirements (tied to contracts and regulation) |

Why: the basic shape of convention design is separating "business decisions" (values agreed with the customer) from "technical decisions" (applying established practice), and delegating only the latter to AI plus deterministic checks.

## Step 0: Inventory conventions and triage for translation

Take each existing (or desired) convention and sort it into one of three buckets:

1. **Deterministically enforceable** → tool config (formatting, import order, dependency direction, naming patterns, type strictness)
2. **Needs semantic judgment** → LLM review checklist (naming quality, abstraction level, pattern conformance)
3. **Business decision** → human approval gate (ubiquitous language, public API changes, architecture changes)

Why: deterministically enforceable rules can be made strict at near-zero cost. Rules that need human judgment must be few — the more rules there are, the lower the compliance rate per rule.

Triage test: "Can a violation of this convention be detected mechanically, by text pattern or AST?" If yes, it is bucket 1. **As a rule, do not create a convention that cannot become a config file.**

## Step 1: Lay down the starter kit (day one of the project)

Every new repository gets this standard set on day one. Maintain it as a template shared across projects and roll it out on the start date:

- [ ] **Formatter** (Prettier / Biome / gofmt / Black / rustfmt) — applied three times over: on save, on commit (lefthook / husky + lint-staged), and in CI
- [ ] **Linter** (ESLint / Biome / RuboCop / golangci-lint / Ruff) — adopt an off-the-shelf style guide (Google Style Guides / PEP 8 / Airbnb / Effective Go) and decide only the deltas where you deviate
- [ ] **Strict typing** (TypeScript strict + ban `as any` + no-floating-promises; mypy --strict; etc.)
- [ ] **Architecture tests** (→ Step 2)
- [ ] **CI gate** (fail the PR on format check / lint / typecheck / test / architecture tests)
- [ ] **Agent hooks** (→ Step 4)

Why: a formatter ends the debate the moment it is configured. A convention document goes stale in three months; a config that fails CI does not.

- Do not write conventions from scratch. Adopting an existing style guide plus documenting the deltas is the fastest path and the best-followed one.
- Full CI pipeline design (deploy and release gates) → sister skill $cicd-release-design.
- Test strategy itself (what to test, how far) → sister skill $test-design.

## Step 2: Introduce architecture tests

Enforce dependency direction, layer violations, and naming patterns *as tests*.

1. **Write each dependency rule as one sentence.** Examples: "importing domain from utils is forbidden"; "the presentation layer must not depend on the infrastructure layer."
2. **Pick a tool for the language:**

   | Language | Tool |
   |---|---|
   | Java / Kotlin | ArchUnit |
   | JS / TS | dependency-cruiser, eslint-plugin-boundaries |
   | Python | import-linter |
   | Go | go-arch-lint |

3. **Start with a single minimal rule.** Encode only the most important layer violation, wire it into CI, confirm green, then add rules incrementally.
4. **Auto-generate dependency graphs** (dependency-cruiser / madge, etc.). Never put a hand-drawn diagram in the docs.

Why: a dependency rule that lives only in a document rots within months. Only rules that fail CI survive.

## Step 3: Keep AGENTS.md minimal

Write down only what tooling cannot enforce.

**What belongs in it:**

- [ ] **A bulleted list of explicit prohibitions** — an explicit NG list beats vague best practices (AI agents comply far better with explicit bans). Examples: "adding `eslint-disable` is forbidden (if needed, state the reason and get human approval)"; "never call an external API inside a transaction"
- [ ] **Domain glossary** (ubiquitous language) — customer's words = code's words = UI's words. Definitions come from the human side (customer agreement)
- [ ] **Files and areas that must not be changed**, enumerated
- [ ] **Verification commands** — the exact commands for lint / typecheck / test / build

**What does not belong in it:**

- Formatting rules (indentation, quotes, line length) → they go in the formatter config. Writing them in a doc wastes tokens
- Restating rules the linter already enforces → double bookkeeping; the moment they drift, both copies lose credibility
- Long passages of generic best practices → they will not be followed. Convert them into prohibitions or delete them

**Writing principles (this section is the source of truth for context-file design):**

- **Keep it thin** — the knowledge body lives in referenced locations (skills, ADRs, docs, references/); AGENTS.md holds only the index and the invariant rules.
- **Pointers over copies** — do not paste code snippets; point with file:line references or "→ see X". Why: pasted code becomes a lie the moment its source changes.
- **No double bookkeeping** — keep the tool-agnostic source of truth in AGENTS.md and make any tool-specific context file a thin wrapper. Never write the same knowledge in two places.
- **Monorepos get a two-tier layout**: root + per-package.

Why: the linter and formatter configs are the source of truth for conventions; the document is supplementary. The longer AGENTS.md gets, the lower the compliance rate per item.

## Step 4: Design agent hooks

Correct during generation, not in after-the-fact review. Wire deterministic checks into your agent's hook mechanism (and CI as the backstop):

- [ ] **On-edit check**: run the formatter + linter automatically after every file edit and feed violations back immediately
- [ ] **Completion gate**: run lint / test / build when the agent finishes work, and block any "done" claim while they fail — enforce via agent hooks where available, and via CI in every case
- [ ] **Disable comments require a reason**: suppression comments (`eslint-disable` and kin) must state a reason; adding one is surfaced in the PR and approved by a human. Unlimited allowance hollows out the convention
- [ ] **Deny dangerous operations**: irreversible actions such as writes to a production DB are excluded from the agent's autonomous execution via deny rules in the hook/permission config

Why: mechanical feedback right after an edit costs orders of magnitude less to fix than a finding at the end of the session.

The verification procedure itself → $verification-loop (source of truth for the six-stage verification flow).

## Step 5: Freeze naming conventions into a single table

Naming is settled by "one table", not by "a debate about principles". Fill this template per project:

| Target | Convention | Example |
|---|---|---|
| Domain-layer types / classes | Ubiquitous-language nouns (match customer terms) | `PurchaseOrder` |
| Use cases / services | Verb + object | `CancelOrderUseCase` |
| Variables / functions | The language's standard case (camelCase etc.) + information-dense names | `remainingStock` |
| DB tables | snake_case, plural | `purchase_orders` |
| DB columns | snake_case | `created_at` |
| Branches | Type prefix + issue number | `feature/123-cancel-order` |
| Commits | Conventional Commits (machine-readable) | `feat(order): add order cancellation` |

- Domain terms must match the ubiquitous language. The term column of the table defers to customer agreement (the human side of the split).
- Any naming pattern that is machine-checkable (case, suffixes) gets translated into linter / architecture-test rules (bucket 1 of Step 0).
- API path and endpoint naming belongs to external design → sister skill $external-design-deliverables.

Why: when conventions differ per project, both human productivity and AI output accuracy drop. One table doubles as the instruction to the AI and the review criterion.

## Step 6: Set the structured-logging convention

Logging conventions are also laid down as logger config + a standard field definition, not as a document.

1. **Require structured (JSON) logs** (pino / zap / slog / structlog / Serilog). Ban string-concatenation logging.
   Why: per-field search, aggregation, and masking only become possible once logs are structured.
2. **Define the standard fields**: `timestamp`, `level`, `trace_id`, `user_id`, `event` + business context. Error logs must carry `trace_id` and the key business identifiers (order ID, etc.).
3. **Fix the level discipline**: ERROR = a human must act / WARN = auto-recovered but watch it / INFO = record of a business event / DEBUG = off in production by default. Keep the discipline that makes "every ERROR pages someone" true — logging everything as ERROR turns alerts into the boy who cried wolf.
4. **Make PII masking a double defense**: first line — keep PII out of logs in the first place (ban whole-object dumps via linter + review); second line — per-field masking plus pipeline-level scrubbing (e.g., an OpenTelemetry Collector processor). Pattern-match detection is only the last line of defense.
   Why: dump a request body wholesale and PII sits in plaintext — during an incident the logs themselves become the secondary leak.
5. **Derive retention from regulation and contract**: as a reference point, PCI DSS expects roughly one year of audit logs with the latest three months immediately available (guideline as of 2026 — verify against the project's actual regulatory requirements). App logs 30–90 days + audit logs one year or more is a realistic starting point for small and mid-size projects. If logs contain personal data, they fall under data-protection law duties — in Japan, the APPI's security-controls and deletion obligations; equivalents elsewhere — so confirm this at contract time.
   This is working practice, not legal advice; final decisions belong to specialists (lawyers, auditors) and customer agreement. Fixing retention and audit requirements is the human side of the split (see the division of labor).

PII definitions and overall data-protection design belong to your compliance / privacy process — hand them there rather than deciding inside this skill.

## Operate as a three-tier gate

Run convention checks in three tiers, each narrower than the last:

1. **Tier 1: deterministic checks** (formatter, linter, types, tests, architecture tests) — finish in seconds, reproduce 100%. Everything enforceable goes here
2. **Tier 2: LLM semantic review** (naming quality, pattern conformance, fit with the convention's intent) — request only what the linter cannot catch, as an explicit checklist of review angles
3. **Tier 3: human approval** (architecture changes, public API changes, new disable comments, ubiquitous-language changes — nothing else) — design the approval flow with your human-in-the-loop / review process

Why: put everything through human review and it stalls; leave everything to the AI and the conventions drift. What sustains is routing each tier only what can be judged nowhere else.

## Anti-patterns (explicit NG list)

- **Writing a splendid convention document without configuring tools** → stale in three months. Tool it before you document it
- **Unlimited `eslint-disable` / `as any`** → hollows out the convention. Require a reason + human approval
- **Dependency rules that live only in docs** → any convention not enforced in code rots within months (→ Step 2)
- **Different conventions per project** → maintain a shared starter kit and apply it on day one (→ Step 1)
- **Logging request bodies wholesale** → becomes a secondary PII leak (→ Step 6)
- **Collapsed level discipline (everything is ERROR)** → real failures get missed (→ Step 6)
- **Formatting rules written into AGENTS.md** → not followed, and a waste of tokens (→ Step 3)

If the same violation keeps recurring, suspect a translation gap — a bucket-1 rule still living as prose → $continuous-learning.

## Completion checklist

Before declaring convention setup complete, confirm with evidence (command output, config files):

- [ ] Formatter, linter, and strict typing are configured, and you have actually seen CI fail a PR on them
- [ ] At least one architecture-test rule is running
- [ ] AGENTS.md contains only what cannot be tooled (no restated formatting rules)
- [ ] Agent hooks (on-edit check / completion gate) are configured
- [ ] The naming table and the logging convention (standard fields + level definitions + masking targets) are in the repository
- [ ] The human-only items (style-guide selection, ubiquitous language, retention periods) are approved
