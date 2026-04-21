---
name: session-handoff
description: Use at the end of every AI coding session to write a structured handoff file. This ensures the next AI agent or model can resume accurately without human re-explanation of context, in-progress files, pending decisions, or known blockers.
---

# Session Handoff

Use this skill at the **end of every session** before closing.

The handoff file is the single most important continuity document in an AI-first codebase. Without it, every new session starts blind.
It complements the maintenance log: the log tracks staged progress over time, while the handoff captures the freshest resume context from this exact session.

## Goal

Overwrite `.agents/last-session.md` with a complete, honest snapshot of this session so the next AI — regardless of model or provider — can resume without asking the human for context.

## When To Run

- at the end of any session where code was read, changed, or decisions were made
- even for planning-only sessions — record what was considered and what was deferred
- even if the session ended early or work is incomplete — especially then

## What To Write

Fill every field. Do not leave fields blank. Write "none" or "n/a" explicitly rather than omitting.

```md
# Last Session Handoff
(overwritten every session — this is not a history file)

- date: YYYY-MM-DD
- model: [model name and version]
- session type: planning | action | mixed

## Task This Session
[one-sentence description of what this session was trying to accomplish]

## Files Modified
[list every file that was changed, even partially]
- path/to/file.js — [brief description of what changed and whether it is complete]

## Files Read But Not Changed
[list files that were read as context — helps next AI know what was already loaded]

## Work Status
[complete | partial | blocked | abandoned]
[if partial or blocked: describe exactly where work stopped and why]

## Pending Decisions
[list any decisions that need user input before proceeding]
- [decision]: [context and why it cannot be resolved by AI alone]

## Discovered But Not Acted On
[list anything found during this session that needs future attention]
- [finding]: [file or area and what was noticed]

## Do Not Touch Next Session
[list any files or areas that are mid-change or fragile right now]
- [file or area]: [reason]

## Recommended First Action Next Session
[exact description of what the next AI should do first]

## Open Ambiguities Added
[list any new entries added to .agents/ambiguities.md this session, or "none"]

## Decisions Recorded
[list any new entries added to .agents/decisions.md this session, or "none"]
```

## Rules

- overwrite the file completely every session — do not append
- write what actually happened, not what was planned
- if work is incomplete, say so explicitly — do not make it sound more complete than it is
- the "Do Not Touch" section is mandatory if any file is mid-refactor
- the "Recommended First Action" must be specific enough for a fresh AI to act on without reading the rest

## File Location

Default: `.agents/last-session.md` in the user's repo root

## Routing

After writing the handoff, also check:
- did this session make a new meaningful decision? → `../decision-registrar/SKILL.md`
- did this session discover a new open question? → `../ambiguity-register/SKILL.md`
- did this session change module structure? → `../blast-radius-mapper/SKILL.md`
