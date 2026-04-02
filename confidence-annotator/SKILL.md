---
name: confidence-annotator
description: Use to add @ai-stable, @ai-uncertain, and @ai-todo inline annotations to code that has been AI-generated or AI-maintained. These signals tell future AI agents which logic has been verified, which was inferred, and what is known to be incomplete — without requiring the agent to read git history or session logs.
---

# Confidence Annotator

Use this skill to annotate code with machine-readable confidence signals.

## Goal

Leave inline markers that tell any future AI agent exactly how much to trust each piece of logic — and what to be careful with — without needing to read the full session history.

## Why This Matters

AI agents cannot feel uncertainty the way humans do. When reading code, everything looks equally "done." Without confidence signals, a future AI editing an uncertain regex has no way to know it was guessed, not specified. A future AI touching a verified core function has no way to know it was confirmed across 5 sessions.

Confidence annotations make the codebase self-describing about its own reliability.

## Annotation Types

### `@ai-stable`
This logic has been verified — by tests, by user confirmation, or by multiple sessions converging on the same result. Do not change without a specific reason.

```js
// @ai-stable: verified by user 2026-03-18, confirmed correct across 3 sessions
function calculateInvoiceTax(amount, rate) { ... }
```

```python
# @ai-stable: matches compliance spec confirmed by user 2026-02-10
TAX_EXEMPT_CODES = ["GOV", "EDU", "MED"]
```

### `@ai-uncertain`
This logic was inferred, guessed, or carried over from a pattern rather than derived from an explicit spec. Verify before relying on it in production or using it as a foundation for further work.

```js
// @ai-uncertain: regex inferred from example data, no formal spec provided — verify with user
const INVOICE_CODE_PATTERN = /^INV-\d{6}$/;
```

```python
# @ai-uncertain: error handling copied from similar module, may not cover all edge cases
def parse_tax_code(raw): ...
```

### `@ai-todo`
This is a known gap — a placeholder, a happy-path-only implementation, or something explicitly deferred. It is not a bug yet, but it is not complete.

```js
// @ai-todo: handles success path only — error and timeout cases deferred by GPT-4o 2026-02-14
async function submitInvoice(payload) { ... }
```

```python
# @ai-todo: pagination not implemented — only returns first page of results
def list_invoices(db, filters): ...
```

## Workflow

1. Select one file or module to annotate (do not annotate the entire codebase in one pass).
2. Read the file in full.
3. For each function, class, or significant block of logic, decide: stable, uncertain, or todo?
4. Check session history (`.agents/last-session.md`, `.agents/decisions.md`) for context.
5. Add annotations — do not change any logic in the same pass.
6. If uncertain logic is also a risk, add a note to `.agents/ambiguities.md`.

## Selection — Which Files To Annotate First

Prioritize:

1. files with HIGH or CRITICAL blast radius
2. files that encode decisions recorded in `.agents/decisions.md`
3. files that have been edited by multiple different AI models
4. files with complex logic and no existing tests

## Rules

- do not change logic while annotating — separate passes only
- one file per run unless files are trivially small
- `@ai-stable` requires a specific verification event (test pass, user confirmation, session convergence) — do not add it speculatively
- `@ai-uncertain` is not a criticism — it is a useful signal; add it freely
- `@ai-todo` must reference the date it was deferred and ideally the model that deferred it
- remove `@ai-uncertain` only when the uncertainty has been genuinely resolved, not just when the code still works
