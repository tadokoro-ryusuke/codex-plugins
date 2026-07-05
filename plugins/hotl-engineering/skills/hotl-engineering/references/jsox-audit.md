# J-SOX / IT General Controls and Audit Response

Control design for advancing AI and automation at a pre-IPO company, and the talking points for
explaining it to auditors.

## Control mapping (implementation in the HOTL workflow)

| Control | Implementation | Evidence |
|---|---|---|
| Change management | Protected branch + PR required + CP2/CP3 approval. Every path to production goes through a PR | PR review logs, Environment approval logs |
| Segregation of duties | Enforce originator (agent/developer) ≠ approver (human) via ruleset. Tier 2 requires a Code Owners review | ruleset configuration values, CODEOWNERS |
| Access management | Eliminate static keys entirely (OIDC federated credentials), least-privilege roles, production secrets scoped per environment | IAM/Entra federation configuration |
| Audit trail | Automatically archive eval reports, deployment records, and review results to immutable storage (e.g., S3 with Object Lock) | Reports in storage (note that CI logs expire after 90 days by default) |
| Program development | Evidence that tests and evals were run is retained as a byproduct of CI | CI results, eval reports |

## How to build the explanation for auditors

- "AI writing code" is not itself the issue. The issue is **"no path exists for an unapproved change
  to reach production."** Keep the ruleset configuration values (empty bypass_actors, required checks,
  approval required) ready to present as-is
- Position AI review and AI evaluation as "tools that assist the control," not "the control itself."
  Show, with a diagram, the structure where the final approver is always a human (CP2/CP3/CP4)
- If asked about the validity of LLM-as-judge: present the human-calibration record (the monthly
  agreement rate). The answer to "AI is evaluating AI" is the existence of the calibration process
- Emergency response (hotfix): Do not keep a permanent bypass; document an operating procedure where
  the ruleset is temporarily disabled and that operation's log itself serves as the evidence

## Limits of segregation of duties in a small team (2-4 people) and compensating controls

Cases where the originator and the approver are the same person are structurally unavoidable. For
audit response:
1. Make the baseline "agent originates + human approves" (formal separation always holds)
2. For Tier 2 (auth, permissions, migrations, confidentiality boundaries), require review by a
   different human
3. Each month, sample-review the approval status of all merges and keep a record (a detective control)
4. Document the above as control documentation (policy / procedure), build up an operating track
   record, and only then face the audit

## AI-specific controls to prepare ahead of time

- A register of agent permissions (which workflow can access what, under which role)
- Documentation stating that change management for prompt and model changes (eval-gate + CP4) is
  included under "program change management"
- Evidence in the role configuration that the incident-investigation agent is Read-Only
- A list of the scope and conditions for operations that "run without human approval," such as
  automatic rollback and auto-merge
