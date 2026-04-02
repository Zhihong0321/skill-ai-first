---
name: architecture-optimizer
description: Use when an AI-maintained codebase has already been stabilized enough for one focused structural improvement. This skill optimizes one big-picture problem at a time, such as duplicate logic, mismatched module boundaries, outdated abstractions, or data flow that no longer fits the current product.
---

# Architecture Optimizer

Use this skill for one focused structural improvement after baseline, mapping, and early cleanup have made the system readable enough to reason about.

## Goal

Improve the big-picture shape of the codebase without turning the run into a full overhaul.

## Good Targets

- duplicate business rules in multiple modules
- outdated abstractions that now add more confusion than value
- competing data flow paths
- weak boundaries between service, controller, and view layers
- earlier decisions that no longer match the current product direction

## Workflow

1. Confirm one architecture target.
2. Read `../references/anti-overengineering.md` — confirm the improvement removes complexity rather than adds a new layer.
3. Describe the current mismatch in plain language.
4. Define the intended simpler shape.
5. Make one structural improvement.
6. Verify behavior did not regress.

## Rules

- one architecture problem per run
- do not combine with repo-wide cleanup
- do not jump to overhaul when a focused simplification is enough
- prefer deletion of duplicate logic over adding another abstraction
- if the improvement introduces a new pattern, interface, or layer that has only one concrete user today, stop — read `../references/anti-overengineering.md`

## Escalation Threshold

If the improvement requires changes across more than **3 files** or touches more than **2 distinct modules**, stop.

- do not proceed with the change in the same run
- route to `../overhaul-planner/SKILL.md` instead
- record the escalation decision and reason in the maintenance log

## Deliverable

Report:

- the old structural problem
- the chosen improvement
- why the new shape is easier for future AI agents to work with
- what next optimization, if any, now becomes possible
