# AI First Codebase Management

Multi-skill bundle for staged maintenance and full AI-first operation of AI-maintained codebases.

## Purpose

This bundle is designed for repos developed by AI coding agents. It has two layers:

**Layer 1 — Maintenance discipline** (stop bad AI behavior):
- single-task-per-run workflow
- staged cleanup and refactoring
- persistent maintenance log

**Layer 2 — AI-first operating system** (make good AI behavior automatic):
- session memory and cross-session handoff
- decision log to prevent reversing hard-won choices
- per-module contracts to prevent scope drift
- blast radius awareness before structural changes
- confidence annotations embedded in code
- model routing for multi-model teams
- known-unknowns register to prevent AI overconfidence

## Layer 1 — Maintenance Skills

- `ai-first-maintenance`: automation-friendly entrypoint — say "run ai-first-maintenance"
- `maintain-ai-first-codebase`: top-level strategy and stage selection
- `baseline-locker`: confirm and protect current working state
- `codebase-mapper`: build a ranked maintenance map
- `file-digester`: split one oversized or overloaded file
- `residual-cleaner`: remove or soft-remove one residual target
- `architecture-optimizer`: improve one structural problem at a time
- `overhaul-planner`: plan a subsystem overhaul without rushing implementation

## Layer 2 — AI-First Operating Skills

- `session-handoff`: write `.agents/last-session.md` at the end of every session
- `decision-registrar`: record WHY choices were made in `.agents/decisions.md`
- `context-navigator`: build `.agents/nav.md` — what to read for each task type
- `blast-radius-mapper`: map what breaks when a module changes — `.agents/blast-radius.md`
- `contract-writer`: add `@ai-contract` headers to modules to define scope boundaries
- `ambiguity-register`: track known unknowns in `.agents/ambiguities.md`
- `confidence-annotator`: add `@ai-stable / @ai-uncertain / @ai-todo` inline signals
- `model-router`: maintain task-to-model routing in `.agents/model-routing.md`

## Shared Resources

- `references/`: policy files used across all skills
- `scripts/`: audit and utility scripts
- `templates/`: ready-to-copy templates for all `.agents/` memory files

## Scripts

- `scripts/inventory_large_files.py`: rank files by size for digestion review
- `scripts/find_context_noise.py`: detect stale/temp/legacy filename patterns
- `scripts/update_maintenance_log.py`: initialize or append the maintenance log
- `scripts/find_missing_contracts.py`: find modules without `@ai-contract` headers
- `scripts/find_importers.py`: find all files that reference a given module (for blast radius)

## The `.agents/` Memory Layer

The bundle expects the user's repo to maintain these files under `.agents/`:

| File | Purpose | Skill |
|------|---------|-------|
| `ai-first-maintenance-log.md` | Staged maintenance history | `ai-first-maintenance` |
| `last-session.md` | Handoff from the last AI session | `session-handoff` |
| `decisions.md` | Architectural decision log | `decision-registrar` |
| `nav.md` | Task-to-reading-list index | `context-navigator` |
| `blast-radius.md` | Module impact map | `blast-radius-mapper` |
| `ambiguities.md` | Known unknowns register | `ambiguity-register` |
| `model-routing.md` | Task-to-model routing table | `model-router` |

Templates for all these files are in `templates/`.

## Suggested Usage

Fast entry:

- say `run ai-first-maintenance`

- either recommend that target or execute it, depending on the user's request

Direct strategy entry:

- use `maintain-ai-first-codebase` and let it choose the next stage

Default sequence:

1. `baseline-locked`
2. `map-ready`
3. `digestion-ready`
4. `cleaning-ready`
5. `optimization-ready`
6. `overhaul-ready`

## Installation Notes

This repository is published as a multi-skill bundle.

- Keep the folder structure intact so sibling skill references continue to work.
- For project-local usage, place the repo contents under `.agents/skills/`.
- For personal usage, place the repo contents under your Codex skills directory if your setup supports multi-skill bundles there.
- If you install a single folder in isolation, also copy the shared `references/` and `scripts/` directories it depends on.
- The bundle expects to maintain a repo-local memory file at `.agents/ai-first-maintenance-log.md`.
