---
name: cicd-release-design
description: "CI/CD pipeline and deploy/release strategy design: staged quality gates (lint/typecheck/test/E2E/security), GitHub Actions workflows, secrets management (OIDC keyless, Environments, Vault), SHA-pinned actions, least-privilege GITHUB_TOKEN, branch protection, deploy strategy selection (blue/green, canary, rolling, managed PaaS), feature flags, rollback runbooks, expand-contract migrations. Reference skill; invoke explicitly with $cicd-release-design when building a pipeline, choosing a deploy strategy, designing a release flow, writing a rollback plan, or reviewing any of these."
---

# CI/CD & Release Design

**Iron rule: separate deploy (putting code in production) from release (showing the feature to users).**

CI/CD is an up-front investment made the moment the repository is created; it sets the floor for the speed and quality of everything that follows.
In a solo-developer + AI-agent setup, CI is the quality supervisor that is always awake on the human's behalf — an agent's output becomes trustworthy only after it passes the CI gates.

Measure the design with the DORA Four Keys (deployment frequency, lead time for changes, change failure rate, MTTR).
Why: so pipeline quality is discussed in industry-standard metrics, not gut feeling.

## Deliverables every design must produce

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
| On PR | lint + typecheck + unit | a few minutes |
| On merge | integration + build | — |
| Pre-release | E2E + security scans | — |

- Tune thresholds to balance developer friction against safety — e.g. fail the build only on critical/high vulnerabilities.
- Coverage ratcheting (never lower the bar) and flaky-test quarantine rules are owned by the sister skill → $test-design (its operating rules and test-plan review checklist). CI owns the mechanical enforcement: threshold gates, quarantine labels, skip procedure.
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
  Why: one survey reports ~61% of organizations have exposed secrets in public repositories (rough figure — verify).
- [ ] Enable automated dependency updates (Dependabot/Renovate). Add SLSA / SBOM when the client's security requirements call for them.

## Step 3: Build one standard template, clone it into every project

Do not write a pipeline from scratch per project.
Why: for a solo contractor, cloning a template is the single biggest efficiency win. CI plumbing is not a differentiator — do not sink time into it.

- [ ] Go all-in on managed CI (GitHub Actions / GitLab CI). Do not self-host Jenkins.
- [ ] **Consolidate verification commands into package.json / Makefile / justfile** so local and CI run the exact same commands.
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
| Managed PaaS built-ins | Cloud Run traffic splitting, Vercel skew protection, etc. | Almost no extra gear needed | Limited to platform features | The majority of small projects |

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
- [ ] Require human approval whenever the write target is production, the operation is irreversible, or the cost of an error exceeds the cost of a review.
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
- **Triggering a rollback**; customer-facing impact notices
- Final say on secrets/permission design (including the agent's own permissions)

Why draw the line: keeping irreversible production operations out of autonomous agent execution and requiring a human in the loop is the practical consensus as of 2026 (verify against current guidance).

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
