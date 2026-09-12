# Screen design

Start at the level needed by the task: screen inventory, transitions, wireframes,
or detailed specs. A useful order for unresolved structure is screen list →
transitions → wireframes → specs. Reuse accepted structure and user-requested
fidelity; do not replay every stage or stop after each draft for approval.

Structure around business objects where list → detail → actions fits the work.
Use task-oriented flows where the actual user journey requires them. Explain a
material information-architecture choice with the business flow it supports.

Use stable screen IDs so names can change without breaking references. Record
physical field names when known, separately from display labels. Cross-reference
the authoritative permission matrix, define validation conditions and error
behavior, and state URL parameters and initial-display conditions.

| Screen ID | Name | Purpose | Target roles | URL | Permission reference |
|---|---|---|---|---|---|
| SCR-010 | Project list | Find projects in own organization | viewer and above | /projects | PERM-project-view |

Cover relevant error, empty, no-permission, and recovery paths in transitions or
per-screen state lists. Keep modals, tabs, and other local states visible in the
spec when a screen-level diagram cannot explain them.

Use tables and Mermaid when they make the spec readable and maintainable; use the
project's existing design tool for layouts. Maintain one source for decisions,
linking a visual artifact to its spec instead of duplicating contradictory copies.

Label prototype evidence accurately. State which interactions are simulated,
which integrations exist, and which behaviors remain unverified. Match the note
to the actual artifact instead of asserting that all processing is always absent.
Visual completeness alone does not establish persistence, permissions, recording,
synchronization, or other runtime behavior.
