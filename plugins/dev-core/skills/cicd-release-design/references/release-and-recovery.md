# Release and recovery

Choose a rollout mechanism from service impact, traffic, coexistence requirements,
recovery time, platform capabilities, and operational cost. Reuse managed rollout
controls where they satisfy those requirements.

| Mechanism | Decision constraint |
|---|---|
| Blue/green | Maintain two environments and verify switching plus data compatibility |
| Canary | Observe a limited audience with meaningful stop criteria and old/new coexistence |
| Rolling | Preserve compatibility while instances are replaced gradually |
| Managed platform rollout | Check the provider's actual traffic, version, and rollback semantics |

Choose a release window with the incident-response coverage the change needs;
do not impose a calendar rule irrespective of staffing. Address staging/production
drift through the project's configuration and infrastructure controls.

## Desktop and mobile distribution

Use update channels and staged binary distribution rather than server traffic
percentages. Include platform signing, notarization, or store review in the relevant
gates. Protect signing keys and document backup/rotation against the updater's
actual trust model; key loss can block updates for installed clients.

Plan recovery as a new signed release of a known-good version where needed.
Already-installed binaries generally cannot be reverted by a server traffic switch.
Verify updater behavior on the required devices separately from package creation.

## Feature flags

Use flags when exposure must be separated from deployment. Record purpose, owner,
type, removal or review date, and rollback behavior. Release and experiment flags
usually have an end condition; operational kill switches and entitlements may be
long-lived. Define experiment stopping criteria from the agreed analysis plan
rather than waiting indefinitely for significance.

Test meaningful enabled/disabled and coexistence behavior. Audit on the team's
maintenance cadence; do not create a new flag platform or recurring task solely
because this reference lists one.

## Migrations and recovery criteria

For schema changes with mixed-version operation or code rollback requirements,
use expand → support old and new → contract. Delay removal until the old consumers
and rollback window are retired. Define backfill, verification, and data recovery;
rolling back code alone does not reverse an incompatible or destructive data change.

Before exposure, specify failure signals, thresholds, observation window, and who
or what may stop, roll back, or roll forward. For high-risk changes, prepare and
validate the concrete recovery procedure before deployment. Choose rollback versus
roll-forward from data safety and recovery time, not a universal preference.

Keep promotion and recovery within recorded authority. Preserve explicit human
gates and preauthorized automated recovery conditions. Do not weaken review
protections or widen the agent's permissions to complete its own deployment.
Customer-facing notices require their own authorization.
