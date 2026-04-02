---
name: model-router
description: Use to build and maintain the model routing table at .agents/model-routing.md. Maps task types to recommended AI models based on their strengths and the project's history. Essential when multiple AI models — across different providers and versions — contribute to the same codebase.
---

# Model Router

Use this skill to build and maintain the model routing table.

## Goal

Produce or update `.agents/model-routing.md` so that the human (and AI agents advising on task assignment) can route each task type to the most capable model — and so the codebase records which model generated which part of the system.

## Why This Matters

Different models have different strengths:

- context window size varies — some models handle large files better
- instruction-following quality varies by model and task type
- some models reason better, some generate faster, some are more cautious
- models drift over time — GPT-4o in 2026-01 ≠ GPT-4o in 2026-06

Without a routing table, every task goes to whatever model is open — and the codebase accumulates inconsistencies, conflicting styles, and unknown assumptions.

## When To Run

- at the start of a new project or when a new model is introduced
- when a model change causes unexpected behavior or regression
- after discovering that a particular model is consistently weak on a task type
- periodically as a maintenance pass when the model roster changes

## Routing Table Format

```md
# Model Routing

## Task → Model Map

| Task type | Recommended model | Reason | Last reviewed |
|-----------|------------------|--------|--------------|
| Large file refactoring (>300 lines) | [model] | [why] | YYYY-MM-DD |
| New feature implementation | [model] | [why] | YYYY-MM-DD |
| Architecture planning | [model] | [why] | YYYY-MM-DD |
| Writing tests | [model] | [why] | YYYY-MM-DD |
| Cleanup and residual removal | [model] | [why] | YYYY-MM-DD |
| Touching payment or auth code | human-approved only | too high risk | YYYY-MM-DD |
| Codebase mapping and navigation | [model] | [why] | YYYY-MM-DD |
| Session handoff writing | any | low risk | YYYY-MM-DD |

## Models Active On This Codebase

| Model | Period | Areas of ownership | Known tendencies |
|-------|--------|-------------------|-----------------|
| [model name] | YYYY-MM → YYYY-MM | [modules] | [e.g., tends to over-abstract, good at tests] |

## Do Not Use [model] For

- [task type]: [reason — regression, known weakness, etc.]
```

## Workflow

1. Review the models that have contributed to the codebase (check `.agents/decisions.md` for model attribution).
2. Identify the task types most common in this project.
3. For each task type, assign a recommended model based on known strengths.
4. For high-risk task types, mark as "human-approved only."
5. Record known tendencies and weaknesses for each model — these are as important as strengths.

## Rules

- this file is human-owned — AI agents write draft entries, humans approve
- task routing is a recommendation, not a hard lock
- "human-approved only" must be used for any task touching payment, auth, identity, or compliance
- track model tendencies honestly — if a model over-abstracts, say so
- update when a model version changes significantly (e.g., GPT-4o → GPT-5)

## File Location

`.agents/model-routing.md` in the user's repo root.
