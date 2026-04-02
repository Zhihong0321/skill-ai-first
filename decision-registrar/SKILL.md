---
name: decision-registrar
description: Use when a meaningful architectural, structural, or design decision is made during any maintenance or coding session. Records the decision, reasoning, rejected alternatives, and stability status so future AI agents do not accidentally reverse deliberate choices.
---

# Decision Registrar

Use this skill whenever a non-trivial decision is made about how the codebase is structured or why something works the way it does.

## Goal

Append one entry to `.agents/decisions.md` so that any future AI — regardless of model, session, or provider — understands what was decided and why, and does not reverse it without explicit user approval.

## When To Record

Record a decision when:

- a module is structured in a specific way for a specific reason (not just convenience)
- a simpler or more obvious alternative was considered and rejected
- a future AI reading the code might reasonably ask "why isn't this done differently?"
- a hard-won constraint applies (compliance, performance, scaling, audit trail)
- a module is intentionally kept monolithic, split, or otherwise unusual

Do not record:
- trivial naming or formatting choices
- decisions that are already obvious from the code itself
- implementation details with no architectural significance

## Entry Format

```md
## YYYY-MM-DD — [short decision title]

- made by: [model name and version]
- reason: [plain-language explanation — why this, not something else]
- rejected alternatives:
  - [alternative 1]: [why it was not chosen]
  - [alternative 2]: [why it was not chosen]
- constraints it encodes: [compliance, performance, scaling, etc. — or "none"]
- files affected: [list of files where this decision is encoded]
- do not reverse without: [what the human or AI must do before changing this]
- status: STABLE | ACTIVE | PROVISIONAL | SUPERSEDED
```

## Status Definitions

- **STABLE**: decision is settled and should not be changed without a clear new requirement
- **ACTIVE**: decision is in effect and is being relied upon by current code
- **PROVISIONAL**: decision was made under uncertainty — revisit before next major change
- **SUPERSEDED**: decision was replaced by a newer entry — kept for historical reference

## File Location

`.agents/decisions.md` in the user's repo root. Append-only — never delete old entries, mark as SUPERSEDED instead.

## Rules

- one entry per decision, not per session
- write for a future AI that has never seen this codebase
- if the reason is "we don't know yet," do not record a decision — record an ambiguity in `.agents/ambiguities.md` instead
- if a decision is reversed, mark the old entry SUPERSEDED and add a new entry explaining the change
