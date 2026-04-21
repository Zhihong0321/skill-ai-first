---
name: contract-writer
description: Use to add @ai-contract headers to modules in an AI-maintained codebase. Contracts define what each module is for, what it must not do, and what it accepts and emits — so future AI agents can reason about boundaries without reading the full implementation.
---

# Contract Writer

Use this skill to embed machine-readable contracts into module headers.

## Goal

Give every significant module a contract header that any AI agent can read in seconds to understand:

- what this module is for
- what it is not allowed to do
- what it accepts and emits
- how stable it is

## Why Contracts Matter

Without contracts, modules drift. Each AI session adds a little more to a file that was supposed to do one thing. After 20 sessions across 3 models, the file does 6 things. No future AI can tell which behavior was intentional.

A contract defines the boundary. Any AI that violates the contract is doing something wrong, even if the code works.

## Contract Format

Place the contract at the very top of the file, before any imports.

**JavaScript / TypeScript:**
```js
/**
 * @ai-contract
 * PURPOSE: [one sentence — what this module is for]
 * MUST NOT: [what this module is explicitly forbidden from doing]
 * ACCEPTS: [inputs — parameters, events, or data formats]
 * EMITS: [outputs — return values, events, side effects]
 * STABLE SINCE: YYYY-MM-DD
 * LAST REVIEWED: YYYY-MM-DD by [model name]
 */
```

**Python:**
```python
# @ai-contract
# PURPOSE: [one sentence]
# MUST NOT: [explicit prohibitions]
# ACCEPTS: [inputs]
# EMITS: [outputs or side effects]
# STABLE SINCE: YYYY-MM-DD
# LAST REVIEWED: YYYY-MM-DD by [model name]
```

## Selection — Which Modules To Contract First

Prioritize in this order:

1. modules with HIGH or CRITICAL blast radius (see `.agents/blast-radius.md`)
2. modules touched most frequently across sessions
3. modules that encode a key decision (see `.agents/decisions.md`)
4. any module that is a likely future digestion or optimization target

## Workflow

1. Read `.agents/blast-radius.md` to identify priority targets.
2. Read the target module in full.
3. Write the contract — be honest about MUST NOT, not aspirational.
4. Add the header. Do not change any logic in the same pass.
5. If writing the contract reveals that the module already violates its own intended boundary, note it in `.agents/ambiguities.md` — do not silently fix it.

## Rules

- one module per run unless they are trivially small
- do not change logic while adding contracts — separate passes only
- MUST NOT must be concrete, not vague (e.g., "MUST NOT call external APIs" not "MUST NOT do too much")
- STABLE SINCE is the date the contract was written, not the date the file was created
- update LAST REVIEWED whenever the contract is re-read and confirmed as still accurate
- contracts describe what the module IS today — not what it could be, should be, or might become
- if writing the contract reveals the module already does too much, note it in `.agents/ambiguities.md` — do not silently redesign it
- read `../references/anti-overengineering.md` if you feel tempted to write a contract for a module that does not yet exist

## Use `../scripts/find_missing_contracts.py`

This script scans the repo and lists modules that do not yet have an `@ai-contract` header, sorted by file size. Use it to prioritize contract writing work.

## Richer Alternatives
`@ai-contract` is compact and machine-readable — suitable for any module.
For modules that also need domain context, fragile-area warnings, or tried-and-rejected history, use the fuller formats in `../ai-first-codebase/`:

- `templates/file-header.md` — WHAT / WHY / OWNS / NOT / DANGER header (replaces or supplements `@ai-contract`)
- `templates/CONTEXT-template.md` — full module briefing file including business rules, dependency map, and glossary
