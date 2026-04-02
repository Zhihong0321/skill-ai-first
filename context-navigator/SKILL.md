---
name: context-navigator
description: Use to build or update the codebase navigation index at .agents/nav.md. Maps task types to required reading lists so any AI agent can load exactly the right context for a given task without over-reading or guessing. Essential for large projects with many modules.
---

# Context Navigator

Use this skill to build and maintain the reading map for the codebase.

## Goal

Produce or update `.agents/nav.md` so that any AI agent starting a new session can answer "what do I read first?" for any common task type — without loading unnecessary files into context.

## Why This Matters

Context windows are finite. On large projects, loading the wrong files wastes budget and causes errors. Without a nav index, an AI either over-reads (slow, expensive) or under-reads (dangerous, incomplete picture). The nav index solves this.

## When To Run

- after any significant structural change (new module, file split, new subsystem)
- when a new task type is introduced that is not covered by existing entries
- during a `map-ready` stage pass as an output alongside the maintenance map
- whenever a future AI would struggle to know what to read for a common task

## What To Build

For each task type, define:

```md
## [Task type label]

- must read: [list of files, always load these first]
- should read: [conditionally useful — load if task touches this area]
- do not touch without reading: [high-risk files that need context before editing]
- owner module: [the primary file responsible for this concern]
- blast radius note: [brief risk summary — or see blast-radius.md]
- last updated: YYYY-MM-DD
```

## Example Entry

```md
## Authentication and session management

- must read: src/auth/session.js, src/auth/token.js, src/middleware/auth-guard.js
- should read: src/config/auth-config.js
- do not touch without reading: src/auth/token.js (JWT signing — see decisions.md 2026-02-10)
- owner module: src/auth/session.js
- blast radius note: auth changes propagate to every protected route — HIGH risk
- last updated: 2026-04-02
```

## Workflow

1. Inspect the current repo structure and recent maintenance map if available.
2. Identify the 5–10 most common task types for this codebase.
3. For each task type, trace the key files by reading entry points and imports.
4. Write or update the entry in `.agents/nav.md`.
5. Keep each entry short — this is a pointer, not a full analysis.

## Rules

- keep entries brief — max 6 lines per task type
- do not describe what files do — describe when to read them
- update entries immediately when module boundaries change
- if a task type spans more than 8 files in "must read," the module needs digestion first

## File Location

`.agents/nav.md` in the user's repo root.
