---
name: overhaul-planner
description: Use when an AI-maintained codebase has a subsystem whose structure is no longer valid and smaller refactors are no longer enough. This skill plans a deliberate overhaul with clear scope, risks, and sequencing rather than letting the AI rush into a large rewrite.
---

# Overhaul Planner

Use this skill only when smaller staged work is no longer enough.

## Goal

Plan a deliberate overhaul of one subsystem without implementing the entire redesign in the same run.

## When To Use

Use only when:

- digestion would only move complexity around
- cleanup would not solve the structural mismatch
- optimization would still leave the subsystem fundamentally wrong

## Disqualifiers — Do Not Overhaul If

Check these before proceeding. If any disqualifier is true, return to an earlier stage instead.

- a single digestion pass would unlock 80% of the problem → use `file-digester` first
- the subsystem is unclear because of noise, not because of structural failure → use `residual-cleaner` first
- the problem is duplicate logic that can be merged cleanly in one focused pass → use `architecture-optimizer` first
- the subsystem has not yet been baselined or mapped → complete those stages first
- the overhaul scope cannot be described in one sentence → the target is too large; split into smaller subsystems

If none of the disqualifiers apply, overhaul planning is justified. State which disqualifier checks were performed and why each was cleared.

## Workflow

1. Define one subsystem candidate.
2. Explain why smaller stages are insufficient.
3. Describe current constraints and risks.
4. Propose the minimum viable overhaul shape.
5. Break the overhaul into future stages.

## Rules

- planning only by default
- no full rewrite in the same run unless explicitly requested
- keep scope tight
- prefer phased migration over hard replacement

## Deliverable

Produce an overhaul brief with:

- target subsystem
- why overhaul is justified
- boundaries of the redesign
- phased sequence for future work
