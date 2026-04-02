---
name: blast-radius-mapper
description: Use before any structural change to map what else would be affected. Builds and maintains .agents/blast-radius.md so AI agents know the cost and risk of changing any given module before touching it. Prevents silent breakage in large, multi-module codebases.
---

# Blast Radius Mapper

Use this skill before structural changes, or to maintain the blast radius index after modules change.

## Goal

Know the cost of a change *before* making it. Produce or update `.agents/blast-radius.md` with an importers map and risk classification for each significant module.

## When To Run

- before any digestion, cleanup, or architecture change
- after any file is split, renamed, or moved
- during the `map-ready` stage as part of building the maintenance map
- whenever the "do not touch" warnings in `nav.md` need to be updated

## How To Map

For each significant module:

1. Search for all files that import, require, or reference it directly.
2. Trace one level further: what imports those importers?
3. Classify risk based on importer count and criticality.
4. Write the entry.

**Search approach:**

```bash
# Find direct importers (adjust pattern for language)
grep -r "from './invoiceRepo'" src/
grep -r "require.*invoiceRepo" src/
grep -r "import.*invoice_repo" src/   # Python
```

Use `../scripts/find_importers.py <file>` if available.

## Entry Format

```md
## [relative/path/to/module.js]

- direct importers: [count] — [list of files]
- indirect reach: [count of modules that depend on importers]
- risk level: LOW | MEDIUM | HIGH | CRITICAL
- risk reason: [why — payment path, auth, shared utility, etc.]
- safe to refactor: yes | yes with verification | only with user approval
- last mapped: YYYY-MM-DD
```

## Risk Classification

| Level | Criteria |
|-------|---------|
| LOW | ≤2 importers, not in critical path |
| MEDIUM | 3–8 importers, or any importer in critical path |
| HIGH | >8 importers, or direct path to payment/auth/data |
| CRITICAL | Core shared utility imported across the entire codebase |

## Rules

- a CRITICAL or HIGH module must not be changed without user approval
- if blast radius is unknown, classify as MEDIUM until mapped
- update entries immediately after any structural change
- do not let the map go stale — an outdated blast-radius.md is worse than none

## File Location

`.agents/blast-radius.md` in the user's repo root.

## Routing

After mapping, check if any HIGH or CRITICAL modules are also digestion candidates. If yes, route the human's attention to `../architecture-optimizer/SKILL.md` or `../overhaul-planner/SKILL.md` before any digestion is attempted.
