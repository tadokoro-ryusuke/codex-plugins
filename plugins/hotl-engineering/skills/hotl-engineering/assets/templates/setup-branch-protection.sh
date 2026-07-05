#!/usr/bin/env bash
# =============================================================================
# setup-branch-protection.sh — Batch-configure the main branch ruleset (run in Phase 2)
#
# What this configures (technical implementation of J-SOX change management controls):
#   - Prohibit direct push / force push / deletion on main
#   - Require PR + at least 1 approval + Code Owners review (Tier 2 paths)
#   - Dismiss existing approvals on new commits (prevents swap-after-approval)
#   - required status checks: quality-gate (aggregates the 5 CI layers)
#     * In the latter half of Phase 2, add "ai-review-gate", and for agent-based repos add "eval"
#
# Prerequisites: gh CLI authenticated, admin permission on the target repository
# Usage: ./setup-branch-protection.sh <owner>/<repo>
# =============================================================================
set -euo pipefail

REPO="${1:?usage: $0 <owner>/<repo>}"

gh api "repos/${REPO}/rulesets" --method POST --input - <<'JSON'
{
  "name": "main-protection (HOTL)",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 1,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "require_last_push_approval": true,
        "required_review_thread_resolution": true,
        "automatic_copilot_code_review_enabled": false,
        "allowed_merge_methods": ["squash"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": false,
        "required_status_checks": [
          { "context": "quality-gate" }
        ]
      }
    }
  ],
  "bypass_actors": []
}
JSON

echo "✅ ruleset created for ${REPO}"
echo ""
echo "Next steps:"
echo "  1. Latter half of Phase 2: add 'ai-review-gate' to required_status_checks (also set vars.AI_REVIEW_ENFORCE=true)"
echo "     (for agent-based repos, also add 'eval')"
echo "  2. Set Required reviewers under Settings > Environments > production (CP3)"
echo "  3. Rename .github/CODEOWNERS.sample to CODEOWNERS to activate it"
echo "  4. Keep bypass_actors empty (in an emergency, temporarily disable the ruleset instead,"
echo "     and keep that action's own log as the audit trail)"
