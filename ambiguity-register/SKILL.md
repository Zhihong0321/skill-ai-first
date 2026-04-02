---
name: ambiguity-register
description: Use when an open question is discovered during a session that cannot or should not be resolved by the AI alone. Records known unknowns in .agents/ambiguities.md so future AI agents do not confidently guess the wrong answer to questions that were already known to be unresolved.
---

# Ambiguity Register

Use this skill to record a known unknown before ending a session.

## Goal

Append one entry to `.agents/ambiguities.md` — the do-not-guess list.

The ambiguity register prevents the worst class of AI mistake: confidently resolving something that was already known to be uncertain.

## When To Record

Record an ambiguity when:

- a question arose during the session that affects module structure, data flow, or behavior — but the answer is unclear
- the human has not yet provided direction on something the AI needs to know
- two reasonable approaches exist and neither can be ruled out without more information
- a cleanup or deletion target could be live but callers are external or unknown
- a decision is being deferred — not for caution, but because the answer is genuinely unclear

Do not record:
- questions the AI can answer by reading the codebase more carefully
- preferences with no structural impact
- items already resolved and recorded in `decisions.md`

## Entry Format

```md
## [short title — what the ambiguity is about]

- opened: YYYY-MM-DD by [model name]
- context: [plain description of what was found and why it is unclear]
- options considered:
  - [option A]: [brief description]
  - [option B]: [brief description]
- impacts: [what work is blocked or affected by this ambiguity]
- do not: [what AI agents must not do until this is resolved]
- status: OPEN | RESOLVED | DEFERRED
- resolved by: [leave blank if OPEN]
```

## Resolving Ambiguities

When the human provides a decision on an open ambiguity:

1. Mark the entry `status: RESOLVED`
2. Add `resolved by: [human instruction or model that resolved it, with date]`
3. If the resolution is a meaningful architectural decision, also record it in `.agents/decisions.md`

## Rules

- append only — never delete open entries
- mark RESOLVED explicitly when closed — do not silently remove entries
- reference ambiguities by title in session handoff file if they are blocking work
- if a future AI session discovers the same ambiguity independently, add a note to the existing entry rather than creating a duplicate

## File Location

`.agents/ambiguities.md` in the user's repo root.
