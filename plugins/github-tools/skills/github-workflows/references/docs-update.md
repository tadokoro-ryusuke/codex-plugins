# Documentation Update Workflow

Use this when the user asks to update docs after code changes.

## Flow

1. Inspect changed files and recent commits.
2. Identify affected docs:
   - `README.md`
   - `docs/`
   - API docs
   - examples
   - changelog or release notes if present
   - repo guidance in `AGENTS.md` when the change affects future Codex behavior
3. Update only docs that are now inaccurate or incomplete.
4. Remove references to deleted or deprecated behavior.
5. Add usage examples only when they help a real user perform the changed workflow.
6. Run lightweight checks where available, such as markdown lint or doc build.

## Output

Report:

- Docs changed.
- Code change or behavior that required the doc update.
- Checks run.
- Any doc gaps left intentionally.

