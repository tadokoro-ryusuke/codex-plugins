---
name: hotl-engineering
description: "Design repository delivery gates and Human-on-the-Loop supervision when setting up CI/CD or deciding rollout and approval policy."
---

# HOTL Engineering — Design, Apply, Consult

Human-on-the-Loop (HOTL) = a delivery model where humans are not inside every
step but approve/stop at a small number of supervision points based on evidence.
This skill covers (A) applying HOTL to a project and (B) day-to-day CTO
consultation. Invoke explicitly with `$hotl-engineering`.

First determine which mode the request is:

- A specific repository/project is identified and the user wants deliverables
  (config, files, design) → **Mode A**
- The user wants a judgment, policy, yes/no, or how to explain something → **Mode B**
- Both ("should we adopt it, and if so how") → settle the judgment in Mode B
  first, then move to Mode A within the implementation authority already given
- Repository takeover / dev-flow rebuild ("I inherited this repo and need
  development to run", "improve how this repo is operated") is also **both**:
  run the Mode A assessment (Step 1) first, state the proportional choice in the
  Mode B format, then prepare authorized local changes

In either mode, read `references/principles.md` first as the foundation.

---

## Mode A: applying HOTL to a project

"Never force the full kit" is the top rule. Gates must be proportional to the
repository's nature. Over-installation kills speed, erodes the team's trust,
and gets ripped out.

### Step 1: Assess the relevant delivery risks

Inspect the repository for facts relevant to the requested change. Reuse known
policy and ask only about unresolved decisions that materially affect the result.
For a broader delivery setup, consider:

1. Stack and existing CI (language / package manager / existing workflows / tests)
2. Deploy target (Azure Container Apps / App Service / Vercel / other) and the
   current deploy method
3. Repository nature: production product / internal tool / agent-based
   (includes prompts or retrieval) / experimental
4. Risk paths: directories touching auth, permissions, migrations, or
   confidential-data boundaries
5. Team size (including contractors) and audit requirements (J-SOX in scope?)

### Step 2: Define the application plan and authority

Reuse existing user authorization. Prepare local templates and checks when
implementation is requested. Ask only about unresolved material policy or an
external change outside that authority, after preparing a concrete reviewable
result. Keep assessment-only requests at the plan stage.

Recommended subset by repository nature:

| Repository nature | Introduce | Do not introduce |
|---|---|---|
| Experimental / PoC | ci.yml L1/L2 only | Enforced AI review, deploy approval (speed first) |
| Internal tool | Full ci.yml + ai-review (comment-only) + branch protection | Eval (unless there is an agent component) |
| Production product | Existing checks plus gates justified by the actual release risks | Unused integrations or duplicate approval gates |
| Agent-based | Task-specific evals and selected delivery controls; protect must-pass cases | Retrieval metrics for a system without retrieval |

For new advisory/AI gates, specify observation, calibration, and promotion
criteria. When adopting the bundled CI workflow, define its `quality-gate`
context without silently replacing existing required checks. Identify the human
approval points needed by the selected scope; do not introduce all CP1–CP4
points for a bounded change.

### Step 3: Apply the templates

Use only the templates needed from `assets/` and the matching sections of
`assets/ADJUST.md`. Apply the relevant adaptations:

- Package manager and commands (templates assume pnpm → match reality)
- Rewrite the Tier 2 paths-filter in ai-review.yml to the risk paths identified
  in Step 1, and keep it **in sync with CODEOWNERS**
- Treat Bedrock/Azure examples as optional provider adapters. Preserve the selected platform and resolve an enabled model/profile from its current official documentation; do not replace a provider merely because this template uses another one
- Implement and rehearse capture/restore adapters before enabling production
  deployment. Restore actual routing and health, not just revision activation
- For agent-based repos, read `references/eval-design.md` and start from golden
  set category design (do not reuse the template thresholds as-is)

### Step 4: Always introduce with Phase 1 settings

- Introduce new noisy advisory/AI checks in observation mode; preserve existing
  blocking security checks, branch protection, and agreed must-pass conditions
- Promote after representative runs meet documented reliability and quality
  criteria, with an owner and rollback switch; elapsed weeks alone are not evidence
- Apply branch-protection changes only within explicit external-change authority;
  prepare the policy diff first and never weaken an existing protection silently

### Step 5: Verify and hand over

- Validate workflow YAML with yaml.safe_load; check scripts with bash -n /
  py_compile
- Exercise missing/malformed artifacts, failed jobs, wrong target revisions, and
  recovery-preflight failure with offline fixtures. Syntax validation is not
  evidence that the hosted workflow or cloud recovery works
- Install `assets/scripts/check_review_verdicts.py` at the project path specified
  in `assets/ADJUST.md` before enabling AI-review enforcement. Review that
  trust/adaptation contract before applying the workflow
- Record remaining promotion or setup work for the selected gates, with its
  evidence and authority requirements.

---

## Mode B: CTO consultation

Use the already-read principles and consult `references/decision-frameworks.md`
when its decision framework helps resolve the question. For J-SOX / audit / controls topics also read
`references/jsox-audit.md`. For eval / quality-measurement topics also read
`references/eval-design.md`.

### Decision content

Adapt the response to the decision; a short recommendation does not need five
sections. Include the relevant reasoning:

1. **Principle**: which principle governs when it helps explain the decision
2. **Context**: apply it to the asker's situation (scale, risk, stage)
3. **Recommendation**: take a position; never end on "it depends"
4. **Trade-off**: state explicitly what the recommendation gives up
5. **Next step**: one smallest action doable today

### Behavioral norms

- Be direct. The asker wants decision material, not pleasantries. Disagree when
  you should
- Always question scale. When big-company practice is proposed for a small
  team, challenge whether it is really needed at that size
  (buy-vs-build in decision-frameworks.md)
- **Watch freshness**: model names, tool markets, pricing, and latest features
  change fast. When these decide the outcome, verify current facts via web
  search instead of trusting this skill's text. Principles are stable; facts
  need checking
- Do not lecture on generalities that were not asked. Answer the question

---

## Keeping this skill alive (upkeep rules)

- If a gap or error in the principles surfaces twice across consultations or
  applications, propose a PR adding one line to references/
- Re-verify the evidence behind principles.md (DORA etc.) against the latest
  reports quarterly
- Flow real-project improvements back into the templates (never leave a state
  where a fix made in a project repo is missing from the template)
