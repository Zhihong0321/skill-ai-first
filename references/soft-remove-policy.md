# Soft-Remove Policy

Use soft-remove only when direct deletion is not yet safe enough.

## When To Soft-Remove

- medium confidence that code or files are residual
- live references are unclear
- a small quarantine period is valuable before permanent deletion

For non-code files or whole folders, prefer moving them out of the active path instead of leaving inline markers everywhere.

## Preferred Holding Locations

Use clear, boring locations so future AI agents know where to look:

- `.agents/quarantine/` for temporary holding during a stability window before deletion
- `archive/` for legacy notes, retired folders, or preserved artifacts that should remain accessible but off the active path

If you move a target, preserve a traceable name such as:

- `.agents/quarantine/2026-04-21-old-admin-panel/`
- `archive/legacy-notes-2026-04-21.md`

## How To Mark

Use a clear marker with date and reason.

Examples:

**JavaScript / TypeScript**
```js
// SOFT-REMOVE(2026-04-01): suspected legacy path, no active callers found during cleanup pass
```

**Python**
```python
# SOFT-REMOVE(2026-04-01): suspected legacy helper, no imports found during cleanup pass
```

**Markdown / plain text**
```txt
<!-- SOFT-REMOVE(2026-04-01): outdated instructions, retained one stability window before deletion -->
```

**YAML / config**
```yaml
# SOFT-REMOVE(2026-04-01): obsolete env key, kept for one deploy cycle before removal
```

## Rules

- include the reason, not just the date
- do not soft-remove large unrelated sections in one pass
- do not let soft-remove markers become permanent clutter
- revisit and delete after the agreed stability window
- if you quarantine or archive instead of deleting, record the destination in the maintenance log

## Avoid

- vague markers like "maybe unused"
- hiding meaningful behavior changes inside cleanup
- using soft-remove as a substitute for thinking
