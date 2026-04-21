# Branch Safety Policy

For any maintenance run that can change structure, delete files, move files, or rewrite module boundaries, use a dedicated git branch.

This is the default safe mode for AI-first maintenance.

## Why

A branch makes maintenance:

- easier to review
- easier to abandon if the change is wrong
- safer to resume across multiple sessions
- less likely to contaminate the user's stable branch with half-finished cleanup

## Branch-Required Stages

Use a dedicated branch before taking action in:

- `cleaning-ready`
- `digestion-ready`
- `optimization-ready`
- `overhaul-ready`

It is also recommended for any non-trivial `map-ready` follow-up if the run may create files, move files, or update repo-wide AI memory.

## Branch Naming

Use a short branch name that makes the maintenance target obvious.

Examples:

- `codex/ai-first-cleanup-legacy-notes`
- `codex/ai-first-digest-auth-service`
- `codex/ai-first-optimize-routing-boundary`

## Rules

- do not perform risky structural work directly on `main`
- if the repo already has a suitable feature branch for the target, reuse it
- if the working tree is dirty with unrelated changes, stop and ask before branching or proceeding
- record the branch name in the maintenance log when action work happens
- keep commits small and stage-scoped so rollback stays easy

## If Branching Is Not Possible

If the environment does not support branching or git is unavailable:

- prefer planning mode
- prefer baseline and mapping work over cleanup/refactor
- avoid deletion and major structural changes
- say explicitly in the log that branch protection was unavailable
