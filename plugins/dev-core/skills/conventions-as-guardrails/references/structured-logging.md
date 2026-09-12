# Structured logging

Follow the existing logging platform and define fields around operational questions.
Prefer structured events for service aggregation, correlation, and masking; retain
human-readable local output where that is the actual interface.

Define the event name, severity, correlation identifier, and safe business context.
Include identity fields only when necessary and authorized; do not make personal
identifiers a universal requirement. Keep whole request, credential, or customer
object dumps out of logs. Combine data minimization with field redaction and pipeline
scrubbing; pattern detection alone is a weak last defense.

Define levels and alert routing from operational actionability. An error event does
not automatically require paging; page when the agreed incident criteria are met.
Preserve enough context to investigate failures without expanding sensitive data
collection.

Use the project's approved retention and audit requirements. If they are missing,
prepare options and identify the owner decision; do not impose a generic number of
days or make a compliance claim. For a regulated requirement, verify its current
primary source and applicability with the responsible specialist.

Verify output shape and redaction with representative safe fixtures. State what was
checked locally and what remains unverified in the production logging pipeline.
