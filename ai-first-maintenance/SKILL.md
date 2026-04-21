---
name: ai-first-maintenance
description: Use when the user says "run ai-first-maintenance" or any equivalent. This is the Front Desk — the only skill that should be invoked directly. It reads the repo state, checks the log and last-session file, determines the situation in one pass, and dispatches to exactly one specialist skill. It does not perform any specialized work itself.
---

# AI First Maintenance — Front Desk

This is the **only skill you should invoke directly**.

All other skills in this bundle are specialists. The Front Desk reads the situation and sends you to exactly one of them.

---

## Step 1 — Orient (read these in order, stop when you have enough)

1. **Locate the bundle root** — the directory containing this file.
   All specialist paths below are relative to the bundle root.

2. **Locate the user's repo root** — the project being maintained.

3. **Initialize maintenance memory on first run:**
   If no maintenance log exists in the default or fallback locations, create it immediately:
   ```
   python <bundle-root>/scripts/update_maintenance_log.py --repo-root <repo-root> --init
   ```
   This first-run write is intentional. The bundle is designed for long-running maintenance that may span multiple sessions or weeks.

4. **Check for a session in progress:**
   Read `<repo-root>/.agents/last-session.md` if it exists.
   If work status is `partial` or `blocked` → skip to **Dispatch Rule A**.

5. **Check the maintenance log:**
   Read `.agents/ai-first-maintenance-log.md` (or fallback locations).
   If a stage is marked in-progress → skip to **Dispatch Rule A**.

6. **Run the two inventory scripts** against the repo root:
   ```
   python <bundle-root>/scripts/inventory_large_files.py <repo-root>
   python <bundle-root>/scripts/find_context_noise.py <repo-root>
   ```

7. **Read the last 1–2 log entries** and the stage-selection reference:
   `<bundle-root>/references/stage-selection.md`
   Also read:
   `<bundle-root>/references/branch-safety.md`

---

## Step 2 — Dispatch (pick exactly one rule, top to bottom)

| Rule | Situation | Dispatch to |
|------|-----------|------------|
| **A** | Prior session is partial, blocked, or in-progress | Resume the specialist from `last-session.md` |
| **B** | First run or newly initialized maintenance history | `../baseline-locker/SKILL.md` |
| **C** | Baseline confidence is weak or untested | `../baseline-locker/SKILL.md` |
| **D** | No maintenance map exists or next target is unclear | `../codebase-mapper/SKILL.md` |
| **E** | One file is too large or too mixed to reason about | `../file-digester/SKILL.md` |
| **F** | Clear stale files, dead notes, or temp artifacts exist | `../residual-cleaner/SKILL.md` |
| **G** | Structural shape problem (duplicate logic, bad boundaries) | `../architecture-optimizer/SKILL.md` |
| **H** | Subsystem is fundamentally broken, smaller passes won't fix it | `../overhaul-planner/SKILL.md` |
| **I** | Session just ended or is ending now | `../session-handoff/SKILL.md` |
| **J** | A new architectural decision was just made | `../decision-registrar/SKILL.md` |
| **K** | An open question was discovered that AI must not resolve alone | `../ambiguity-register/SKILL.md` |
| **L** | High-risk module has no `@ai-contract` header | `../contract-writer/SKILL.md` |
| **M** | Blast radius of a planned change is unknown | `../blast-radius-mapper/SKILL.md` |
| **N** | Nav index is missing or stale after structural changes | `../context-navigator/SKILL.md` |
| **O** | Files touched by multiple models have no confidence signals | `../confidence-annotator/SKILL.md` |
| **P** | Model roster has changed or routing decisions are needed | `../model-router/SKILL.md` |

**Stop at the first matching rule. Dispatch to one specialist only.**

---

## Step 3 — After the specialist completes

1. Confirm the specialist wrote its deliverable and performed verification.
2. Update the maintenance log:
   ```
   python <bundle-root>/scripts/update_maintenance_log.py \
     --repo-root <repo-root> \
     --mode action \
     --stage <chosen-stage> \
     --target "<chosen-target>" \
     --reason "<why this target>" \
     --status <planned|in-progress|verification-pending|complete|blocked|deferred> \
     --action "<what was done>" \
     --verification "<what was checked>" \
     --blockers "<blocking issue or none>" \
     --next-action "<exact next step for the next session>" \
     --next-stage "<recommended next>"
   ```
3. If work is incomplete or a decision was deferred, dispatch to `../session-handoff/SKILL.md`.

---

## Rules

- **never perform specialized work directly** — always dispatch to a specialist
- **never dispatch to more than one specialist per run**
- **never skip Step 1** — the log and last-session file are mandatory reads
- **require a branch for risky action stages** — before `cleaning-ready`, `digestion-ready`, `optimization-ready`, or `overhaul-ready`, confirm the repo is on a dedicated branch or switch to planning mode
- **leave a precise resume path** — every run should end with a next exact action, not just a stage label
- if two rules match, pick the one that appears first in the table
- if a specialist's work surfaces a new ambiguity or decision, note it — those are separate dispatches in future runs

---

## Specialist Directory (reference only — do not read these unless dispatched)

| Specialist | What it does |
|-----------|-------------|
| `baseline-locker` | Confirms the current working state is safe before any changes |
| `codebase-mapper` | Builds a ranked maintenance map without touching anything |
| `file-digester` | Splits one oversized or overloaded file into focused modules |
| `residual-cleaner` | Removes one stale, dead, or confusing file or artifact |
| `architecture-optimizer` | Improves one structural problem — bounded to 3 files / 2 modules |
| `overhaul-planner` | Plans a full subsystem redesign when staged passes are insufficient |
| `session-handoff` | Writes the end-of-session handoff file for the next AI |
| `decision-registrar` | Records WHY an architectural decision was made |
| `context-navigator` | Builds the nav.md reading index for common task types |
| `blast-radius-mapper` | Maps what breaks if a given module is changed |
| `contract-writer` | Adds @ai-contract headers to define module scope boundaries |
| `ambiguity-register` | Records a known unknown that AI must not resolve unilaterally |
| `confidence-annotator` | Adds @ai-stable / @ai-uncertain / @ai-todo signals to code |
| `model-router` | Builds and maintains the task-to-model routing table |
| `maintain-ai-first-codebase` | Deep orchestration logic — read only if dispatch logic is insufficient |
