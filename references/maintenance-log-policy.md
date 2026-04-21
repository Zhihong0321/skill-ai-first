# Maintenance Log Policy

The maintenance log is the memory of the bundle.
It must stay useful across long maintenance efforts that may span many sessions or weeks.

Its purpose is to help future AI agents understand:

- what stage the repo is currently in
- what maintenance task was handled last
- what remains in progress
- what should happen next

## Default Log Location

Prefer this path:

- `.agents/ai-first-maintenance-log.md`

Fallback locations only if the repo already uses them:

- `ai-first-maintenance-log.md`
- `docs/ai-first-maintenance-log.md`

On the first run, the bundle may create the default log automatically. This is expected behavior, not accidental repo noise.

## Rules

- update the log on every meaningful maintenance run
- keep entries short and factual
- write what was actually done, not vague intent
- include whether the run was planning-only or action-taking
- if a target is deferred, say why
- write enough detail that a fresh AI can safely resume without reconstructing the session

## Required Fields Per Entry

- date
- mode
- chosen stage
- chosen target
- reason for selection
- status
- action taken
- verification
- blockers
- next exact action
- next recommended stage

## Allowed Status Values

- `planned`
- `in-progress`
- `verification-pending`
- `complete`
- `blocked`
- `deferred`

## Allowed Stage Values

Use the maintenance stage names consistently:

- `baseline-locked`
- `map-ready`
- `digestion-ready`
- `cleaning-ready`
- `optimization-ready`
- `overhaul-ready`

For `next recommended stage`, `none` is also allowed when no further maintenance stage is recommended yet.

## Example Entry

```md
## 2026-04-02

- mode: planning
- chosen stage: map-ready
- chosen target: `src/modules/Invoicing/services/invoiceRepo.js`
- reason: largest active service file and repeated patch layering make later cleanup harder
- status: planned
- action taken: inventoried large files and context-noise candidates; no code edits yet
- verification: inventory scripts completed successfully
- blockers: none
- next exact action: run `file-digester` on `src/modules/Invoicing/services/invoiceRepo.js`
- next recommended stage: digestion-ready
```
