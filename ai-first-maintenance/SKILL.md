---
name: ai-first-maintenance
description: Use when the user wants to run AI-first maintenance on a codebase with one simple prompt such as "run ai-first-maintenance". This entry skill checks the big picture, reads the previous maintenance log if present, determines the current stage, chooses one next target only, and then routes to the appropriate stage skill.
---

# AI First Maintenance

This is the easiest entrypoint for the bundle.

Use it when the user wants the workflow to feel automatic:

- inspect the codebase at a big-picture level
- read the previous maintenance log
- determine the current stage
- choose one next target only
- either recommend that target or execute it if the user clearly asked for action

## Mandatory Startup Workflow

When this skill is invoked:

1. locate the repo root (the user's project being maintained)
2. locate the bundle root (the directory containing this SKILL.md file)
   - script paths like `../scripts/` are relative to the bundle root, NOT the user's repo root
   - resolve: `<bundle-root>/scripts/inventory_large_files.py`, etc.
3. look for an existing maintenance log in the user's repo in this order:
   - `.agents/ai-first-maintenance-log.md`
   - `ai-first-maintenance-log.md`
   - `docs/ai-first-maintenance-log.md`
4. if no log exists, create `.agents/ai-first-maintenance-log.md` using:
   `python <bundle-root>/scripts/update_maintenance_log.py --init --repo-root <repo-root>`
5. read the latest log entries before choosing a stage
6. check if any stage is marked in-progress in the log — if so, resume that stage before choosing a new one
7. run the big-picture inventory against the user's repo root:
   - `python <bundle-root>/scripts/inventory_large_files.py <repo-root>`
   - `python <bundle-root>/scripts/find_context_noise.py <repo-root>`
8. determine the current stage using:
   - `../references/stage-selection.md`
   - the current repo state
   - the last maintenance run log
9. choose exactly one next target
10. route to the appropriate stage skill

## Decision Rules

- if the previous log says a stage is in progress or waiting verification, do not skip ahead casually
- if the repo has never been mapped, default toward `map-ready`
- if very large mixed-responsibility files dominate maintenance friction, prefer `digestion-ready`
- if obvious stale folders, notes, or temp files create immediate confusion, `cleaning-ready` may come first
- if the codebase state is uncertain, return to `baseline-locked`

## Execution Modes

### Planning mode

If the user asks to "run ai-first-maintenance" without explicitly requesting edits:

- inspect
- determine stage
- choose one target
- write a new log entry
- stop with a recommendation

### Action mode

If the user explicitly asks to perform the next maintenance task:

- inspect
- determine stage
- choose one target
- route to the relevant stage skill
- complete that one task only
- update the log

## Logging

Read `../references/maintenance-log-policy.md` before writing the log.

Every run must update the maintenance log with:

- date
- chosen stage
- chosen target
- why the target was selected
- action taken or recommended
- verification status
- recommended next stage

## Routing

- stage decision and orchestration: `../maintain-ai-first-codebase/SKILL.md`
- baseline work: `../baseline-locker/SKILL.md`
- mapping work: `../codebase-mapper/SKILL.md`
- digestion work: `../file-digester/SKILL.md`
- cleanup work: `../residual-cleaner/SKILL.md`
- optimization work: `../architecture-optimizer/SKILL.md`
- overhaul planning: `../overhaul-planner/SKILL.md`
