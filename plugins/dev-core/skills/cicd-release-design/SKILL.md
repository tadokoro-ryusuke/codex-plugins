---
name: cicd-release-design
description: "CI/CD pipeline and deploy/release strategy design: staged quality gates (lint/typecheck/test/E2E/security), GitHub Actions workflows, secrets management (OIDC keyless, Environments, Vault), SHA-pinned actions, least-privilege GITHUB_TOKEN, branch protection, deploy strategy selection (blue/green, canary, rolling, managed PaaS), feature flags, rollback runbooks, expand-contract migrations. Reference skill; invoke explicitly with $cicd-release-design when building a pipeline, choosing a deploy strategy, designing a release flow, writing a rollback plan, or reviewing any of these."
---

# CI/CD & Release Design

**Iron rule: separate deploy (putting code in production) from release (showing the feature to users).**

CI/CD is an up-front investment made the moment the repository is created; it sets the floor for the speed and quality of everything that follows.
In a solo-developer + AI-agent setup, CI is the quality supervisor that is always awake on the human's behalf — an agent's output becomes trustworthy only after it passes the CI gates.

Choose delivery metrics that match the goal and define their measurement window.
Use DORA's current five measures when adopting that framework: change lead time,
deployment frequency, failed deployment recovery time, change fail rate, and
deployment rework rate. Measure one service over time; do not treat them as
individual productivity quotas. Recheck the [DORA definitions](https://dora.dev/guides/dora-metrics/)
when revising the measurement policy.

## Deliverables to select for the requested scope

Reuse existing pipeline and runbook artifacts. Omit non-applicable flag,
migration, or deployment sections with a reason; do not install unrelated systems.

- [ ] Pipeline definition (GitHub Actions workflow YAML / GitLab CI)
- [ ] Quality gate definition (lint / typecheck / test / coverage threshold / SAST / dependency audit / build)
- [ ] Branch protection rules (required checks, mandatory review, no force push)
- [ ] Secrets management design (what lives where, how it is injected, scope of OIDC adoption)
- [ ] Environment definition (dev / staging / production, promotion criteria, Environments approval settings)
- [ ] Release runbook (deploy strategy, verification items, rollback procedure)
- [ ] Feature flag ledger (flag name, purpose, type, removal deadline)
- [ ] DB migration policy (rules that assume expand-contract)

## Step 1: Design quality gates in three stages

Do not run everything on every PR. Staging the checks is the standard play.
Why: piling every check onto the PR pushes it past 15 minutes and stalls development. "Minutes on PR, heavy stuff after merge" buys both speed and safety.

| Stage | Checks | Target time |
|---|---|---|
| On PR | lint, types, focused tests, and affected build/integration/security checks | fast enough for useful feedback |
| On merge | broader regression and packaging checks for the exact merged revision | bounded by project needs |
| Pre-release | remaining runtime, environment, and release-risk checks | before exposure to users |

- Tune thresholds to balance developer friction against safety — e.g. fail the build only on critical/high vulnerabilities.
- Preserve existing coverage gates and investigate flakes before an authorized, owned, time-bounded quarantine; see $test-design. Do not defer a merge-blocking contract/security check merely to keep a preset time budget.
- Test distribution (pyramid), techniques, and test-perspective tables → $test-design.
- Local verification flow → $verification-loop.

## Step 2: Lock down secrets and permissions

Choose in strict priority order; write down the reason whenever you drop a level.

1. **OIDC keyless auth** (GitHub Actions → AWS/GCP/Azure via short-lived tokens; zero long-lived keys stored)
2. **GitHub Environments + approvals** (remaining secrets live here; protect production ones with required reviewers)
3. **HashiCorp Vault / AWS Secrets Manager** (when org requirements or existing infrastructure demand it)

Why: a leaked secret never beats a secret that does not exist. A setup that holds no long-lived keys is the strongest defense.

Mandatory extra hardening:

- [ ] **SHA-pin** every third-party action (tag references are tamperable).
  Why: the March 2025 tj-actions/changed-files compromise (~23k repositories affected) spread through tag references.
- [ ] Declare `permissions:` explicitly and keep **GITHUB_TOKEN least-privilege** (never run on the broad default).
- [ ] Never put secrets in repository variables or committed `.env` files.
  Keep credentials out of source and logs; do not rely on masking after exposure.
- [ ] Enable automated dependency updates (Dependabot/Renovate). Add SLSA / SBOM when the client's security requirements call for them.

## Step 3: Adapt a maintained template to the project

Reuse known commands and controls while checking their assumptions against the
target project. Keep provider-specific adapters explicit and test failure paths.

- [ ] Prefer the project's existing CI service; propose a platform migration only when its benefits justify the scope and operational cost.
- [ ] **Consolidate verification commands into one place** (package.json scripts / Makefile / justfile / cargo aliases / uv + pyproject — follow the stack's standard) so local and CI run the exact same commands. In multi-language repos (Tauri, etc.), bundle every stack behind a Makefile / justfile.
  Why: a CI failure that cannot be reproduced locally doubles debugging cost.
- [ ] Include the flaky-quarantine procedure (label, skip method, reinstatement criteria) in the template.
- [ ] Keep improving the template with feedback from each project and feed it into the next one.
- Root-causing a CI failure itself → $dev-debug.

## Step 4: Pick the deploy strategy by SLA and traffic volume

| Strategy | Mechanism | Strength | Cost / prerequisite | Fits |
|---|---|---|---|---|
| Blue/Green | Two production-grade environments; deploy to the idle one → verify → switch | Rollback is just switching back — instant | 2x environment cost | Larger changes; instant rollback required |
| Canary | Route a few % of traffic to the new version, expand while watching metrics | Smallest blast radius | Design tolerant of old/new coexistence; monitoring maturity | Daily small releases |
| Rolling | Replace instances one by one (Kubernetes default) | Cost-efficient | Long old/new coexistence window | Standard k8s setups |
| Managed PaaS built-ins | Cloud Run traffic splitting, Vercel skew protection, Cloudflare Workers gradual deployments (`wrangler versions upload` -> preview check -> `versions deploy` with % split -> `rollback`), etc. | Almost no extra gear needed | Limited to platform features | The majority of small projects |

**This table assumes server-side deployment.** Desktop/mobile distribution (Tauri, Electron, store apps) follows a different shape:

- Staged rollout is done per **update channel** (stable / beta) and staged updater delivery, not traffic %.
- **Code signing joins the quality gates** (Windows certificate / macOS Developer ID + notarization / store review on mobile). Keep signing and updater keys in CI secrets, and decide the key-backup procedure first — **losing the updater signing key means existing users can never receive another update**.
- **Rollback is a re-release**: prepare a procedure to ship the previous version under a new version number (binaries already on user machines cannot be reverted instantly).

- For most small projects, "**managed-PaaS built-in traffic control + feature flags + an instant-rollback runbook**" is enough. Kubernetes + Argo-grade gear is over-investment.
  Why: safety trades against cost and complexity — decide by the project's SLA and traffic volume.
- Standard combination: **trunk-based + feature flags + canary for daily small releases; Blue/Green only for big cutovers**.
- Avoid Friday-evening deploys. Why: never gamble during the hours when incident-response staffing is thinnest.
- Kill staging/production drift with IaC. Why: divergence between the acceptance environment and production is the leading cause of post-acceptance trouble (in JP contract work, defects surfacing after client acceptance/kenshū).
- Branch workflow choice (GitHub Flow / trunk-based) → $issue-driven-dev.

## Step 5: Manage feature flags by type and lifespan

Classify each flag by type and **set its removal deadline the moment it is created** (Pete Hodgson's "Feature Toggles" taxonomy).
Why: flags without deadlines rot into dozens of dead flags and a combinatorial explosion of branches.

| Type | Purpose | Typical lifespan (per the source) |
|---|---|---|
| Release toggle | Hide unfinished features; staged rollout | Remove within 1–2 weeks |
| Experiment toggle | A/B testing | Until statistical significance (hours to weeks) |
| Ops toggle | Operational switches such as load shedding | Short-lived by default; a kill switch is the permanent exception |
| Permission toggle | Plan/entitlement gating | May be permanent (paid-plan gating lives for years) |

Lifespans follow Pete Hodgson, "Feature Toggles (aka Feature Flags)" (martinfowler.com).

- [ ] A Release toggle that lingers for product reasons is not an exception — always re-set its removal deadline (this skill's operating rule).
- [ ] Maintain the flag ledger (name, purpose, type, removal deadline).
- [ ] **Make a monthly (at minimum quarterly) flag audit a fixed ritual.** Open removal PRs for flags no longer referenced.
- Tooling: choose from LaunchDarkly / Unleash (OSS) / OpenFeature (CNCF standard API).
- Why flags at all: they separate the technical risk of deploying from the business risk of releasing.

## Step 6: Design deploys that can be undone

### DB migrations: expand-contract

Make every schema change in three phases — **add (expand) → support both old and new → remove old (contract)** — staying compatible with one generation back at all times.
Why: if the schema is not backward-compatible, rolling back only the code still breaks. Rollback-ability is effectively decided here.

### Decide rollback criteria before deploying

- [ ] Predefine the trigger (e.g. roll back when error rate exceeds X%). Never go to full rollout on "seems fine".
- [ ] For high-risk changes, **write the rollback command before deploying**.
  Why: the worst pattern is inventing the procedure in the middle of an incident.
- [ ] Rollback vs roll-forward: roll back when immediacy matters; roll forward when data transformations are involved or the hotfix is small.

## Step 7: Design the agent's permissions

When AI agents touch CI/CD, their permission design is a first-class design item of its own.

- [ ] **Pin the final trigger for production deploys to human approval** (GitHub Environments required reviewers).
  Why: "the agent does not touch production while I sleep" is the safe default for a one-person company.
- [ ] Restrict agent tokens to specific write targets.
- [ ] **Protect workflow files with CODEOWNERS.**
  Why: CI is the last line of defense against a runaway agent — the agent must not be able to rewrite the gate itself.
- [ ] Require authority appropriate to the production effect. Preserve existing approval and documented preauthorized recovery conditions; do not ask again for the same approved action.
- General design of human supervision points → $hotl-engineering (separate plugin).

## Division of labor: what AI does / what only humans can decide

### AI (the agent running this skill) does

- Generate and maintain workflow YAML
- First-pass analysis of CI failure logs and fix PRs
- Assist review of dependency-update PRs; triage security alerts
- Generate release notes; first-pass monitoring of post-deploy metrics
- Flag audits (detect unreferenced flags, open removal PRs); migration compatibility checks

### Only humans can decide

- **Quality gate thresholds** (what constitutes failure)
- **Go/No-Go for production releases; approval of promotion to production**
- **Defining rollback authority and thresholds**; authorize bounded automated recovery explicitly, and separately authorize customer-facing notices
- Final say on secrets/permission design (including the agent's own permissions)

Keep these decisions with the owner; execute within the recorded authority.
Do not present a local supervision policy as an industry-wide consensus.

## Review checklist (use during design review)

- [ ] Are quality gates split into three stages, with PR checks finishing in a few minutes?
- [ ] Are secrets OIDC-first? If long-lived keys remain, is the reason written down?
- [ ] Are actions SHA-pinned and GITHUB_TOKEN least-privilege?
- [ ] Do local and CI run the same consolidated commands?
- [ ] Is the deploy strategy neither over- nor under-equipped for the SLA and scale?
- [ ] Are the flag ledger and audit ritual defined?
- [ ] Do migrations follow expand-contract, with rollback criteria predefined?
- [ ] Is there human approval for production deploys and CODEOWNERS protection on workflow files?

## Boundaries with related skills

- Test distribution, techniques, perspective tables, acceptance testing → $test-design
- Local six-stage verification (build→type→lint→test→security→diff) → $verification-loop
- TDD, security principles, coding conventions → $best-practices
- Root-cause analysis of CI failures → $dev-debug
- Issue workflow and branch conventions → $issue-driven-dev
- Turning conventions into automated guardrails (agent hooks / CI enforcement) → $conventions-as-guardrails
- General design of human supervision points and approval flows → $hotl-engineering (separate plugin)

## Canonical resources

- Jez Humble & David Farley, *Continuous Delivery*
- Nicole Forsgren et al., *Accelerate*; DORA State of DevOps Report
- GitHub Docs: "Security hardening for GitHub Actions", "About security hardening with OpenID Connect"
- OWASP CI/CD Security Top 10; SLSA (slsa.dev)
- Pete Hodgson, "Feature Toggles (aka Feature Flags)" (martinfowler.com)
- Ambler & Sadalage, *Refactoring Databases* — the origin of expand-contract
