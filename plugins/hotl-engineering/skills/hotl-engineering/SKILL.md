---
name: hotl-engineering
description: "Design and apply Human-on-the-Loop (HOTL) delivery workflows, and advise on CTO-level decisions for AI-native engineering operations. Apply mode — use for 'introduce quality gates', 'design CI/CD', 'wire AI review into the pipeline', 'build an eval gate', 'set up agent-operation guardrails', 'set up the deploy flow', 'install the HOTL workflow', 'I inherited this repository and need a working dev flow', 'make a small team run development autonomously', 'improve how this repo is operated'. Covers experimental/PoC/personal repos too — pick the proportional subset and push back on over-installation. Consult mode — use for judgment calls: buy-vs-build for AI SRE tools, how much autonomy to grant an agent, enabling auto-merge, explaining AI code quality to auditors, model switches, contractor permissions, J-SOX readiness. Do NOT use for individual coding work (implementing features, fixing bugs or CI failures, refactoring, one-off code reviews)."
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
  first, then move to Mode A after agreement
- Repository takeover / dev-flow rebuild ("I inherited this repo and need
  development to run", "improve how this repo is operated") is also **both**:
  run the Mode A assessment (Step 1) first, present "what to introduce and what
  NOT to introduce" advice in the Mode B format, then apply after agreement

In either mode, read `references/principles.md` first as the foundation.

---

## Mode A: applying HOTL to a project

"Never force the full kit" is the top rule. Gates must be proportional to the
repository's nature. Over-installation kills speed, erodes the team's trust,
and gets ripped out.

### Step 1: Assessment (always do this before proposing)

Investigate the repository and confirm the following. Ask about unknowns in a
single batched question:

1. Stack and existing CI (language / package manager / existing workflows / tests)
2. Deploy target (Azure Container Apps / App Service / Vercel / other) and the
   current deploy method
3. Repository nature: production product / internal tool / agent-based
   (includes prompts or retrieval) / experimental
4. Risk paths: directories touching auth, permissions, migrations, or
   confidential-data boundaries
5. Team size (including contractors) and audit requirements (J-SOX in scope?)

### Step 2: Present the application plan (get user approval before implementing)

Recommended subset by repository nature:

| Repository nature | Introduce | Do not introduce |
|---|---|---|
| Experimental / PoC | ci.yml L1/L2 only | Enforced AI review, deploy approval (speed first) |
| Internal tool | Full ci.yml + ai-review (comment-only) + branch protection | Eval (unless there is an agent component) |
| Production product | Everything (ci / ai-review / deploy+CP3 / incident-triage) | — |
| Agent-based | All of the above + eval-gate (must-pass design required) | — |

The plan must always include: rollout order (comment-only → calibration →
enforcement), consolidating required checks into the single `quality-gate`
context, and where the human approval points (CP1–CP4) sit.

### Step 3: Apply the templates

Copy templates from `assets/` and adapt them to the project following the
checklist in `assets/ADJUST.md`. Main adaptation work:

- Package manager and commands (templates assume pnpm → match reality)
- Rewrite the Tier 2 paths-filter in ai-review.yml to the risk paths identified
  in Step 1, and keep it **in sync with CODEOWNERS**
- Replace the Bedrock model ID with an inference profile enabled in your org
- Rewrite the deploy commands in deploy.yml for the actual platform (keep the
  structure: staging auto → environment approval → health watch → auto rollback)
- For agent-based repos, read `references/eval-design.md` and start from golden
  set category design (do not reuse the template thresholds as-is)

### Step 4: Always introduce with Phase 1 settings

- Keep `continue-on-error: true` on the security layer; do not make AI review a
  required check yet
- Branch protection: PR required + force-push forbidden only
- State in the deliverable README that enforcement starts only after a
  two-week calibration period that eliminates false positives
  (run setup-branch-protection.sh in Phase 2, not Phase 1)

### Step 5: Verify and hand over

- Validate workflow YAML with yaml.safe_load; check scripts with bash -n /
  py_compile
- Attach a "Phase 2 to-do" checklist to the handover (make checks required,
  set environment reviewers, enable CODEOWNERS, initialize the eval baseline)

---

## Mode B: CTO consultation

Read `references/principles.md` and `references/decision-frameworks.md` before
answering. For J-SOX / audit / controls topics also read
`references/jsox-audit.md`. For eval / quality-measurement topics also read
`references/eval-design.md`.

### Answer format

1. **Principle**: which principle governs (cite the number in principles.md)
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
