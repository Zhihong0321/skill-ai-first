---
name: residual-cleaner
description: Use when stale files, dead comments, obsolete notes, backup artifacts, or outdated instructions are lingering in an AI-maintained codebase. This skill removes or soft-removes one residual target at a time so future AI agents face less confusion and less context noise.
---

# Residual Cleaner

Use this skill to resolve one residual source of confusion at a time.

## Goal

Reduce context noise and lingering legacy without risking the current working state.
When deletion is not yet safe enough, prefer quarantine or archive paths that remove noise from the active code path without destroying evidence.

## Valid Targets

- stale markdown notes
- obsolete instructions
- dead folders
- legacy folders that should be preserved outside the active path
- backup artifacts
- temporary scripts
- unreachable code blocks
- commented-out code that no longer serves a purpose

## Confidence Policy

- high confidence: delete directly or archive if retention is still useful
- medium confidence: quarantine, archive, or soft-remove and mark clearly
- low confidence: stop and ask before deleting

Read `../references/soft-remove-policy.md` before using a soft-remove path.

## Workflow

1. Confirm one residual target.
2. Search for live references.
3. Decide delete, quarantine, archive, soft-remove, or defer.
4. Make the smallest clear change.
5. Verify the target is no longer needed.

## Rules

- do not clean multiple categories in one run
- do not mix cleanup with behavior changes
- do not create new scattered notes while removing old scattered notes
- if using soft-remove, include date and reason
- if quarantining or archiving, use a clear repo-local location and preserve the original name or a traceable rename
- record where the target was moved so the next AI can find it fast

## Deliverable

Resolve one residual target and report:

- why it was considered residual
- what confidence level was used
- whether it was deleted, quarantined, archived, soft-removed, or deferred
- the final path if it was moved instead of deleted
