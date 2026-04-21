# AI-First Project Bootstrap Checklist

Use this when starting a new project. Do this at day one, not after the mess accumulates.

---

## Step 1: Root-Level Context (Day 1)

Create these files before writing any source code:

### `CONTEXT.md` (root level)
```markdown
# CONTEXT: [Project Name]

## What this project is
[2-3 sentences: the problem it solves, who uses it, the business model]

## What this project is NOT
[Explicit scope boundaries — what's out of scope now and why]

## Core architectural decisions
[The 3-5 choices that shape everything else — with brief rationale]

## Tech stack
| Layer | Technology | Why chosen |
|-------|-----------|------------|
| [e.g. Backend] | [e.g. Node/TypeScript] | [reason] |

## Key business rules (global)
[Rules that apply across the entire project]

## Glossary (global)
[Terms with project-specific meanings]
```

### `ARCHITECTURE.md`
```markdown
# Architecture

## System overview
[Diagram or description of major components and how they connect]

## Data flow
[How data moves through the system for the main use cases]

## External integrations
[Third-party services used, what they do, constraints on their use]

## Security model
[Authentication approach, authorization model, trust boundaries]

## Scaling model
[Current approach, known limits, plan if we need to scale]
```

---

## Step 2: Module Structure

For each major module/domain, create its directory with:

```
src/
└── [module]/
    ├── CONTEXT.md        ← Create this FIRST, before any source files
    ├── index.ts          ← Re-exports only, minimal logic
    └── [source files]
```

**Write `CONTEXT.md` before the source files.** This forces you to think through:
- What does this module own?
- What are its boundaries?
- What business rules govern it?

You'll write better code when you've articulated this first.

---

## Step 3: Project Conventions File

Create `docs/conventions.md`:

```markdown
# Codebase Conventions

## Naming
- [File naming convention]
- [Function naming convention]
- [Variable naming convention]

## Code style
- [The key style decisions — link to linter config for details]

## Comment conventions
- Use `// WHAT:` / `// WHY:` headers in all non-trivial files
- Use `// DECISION:` for non-obvious architectural choices
- Use `// DO NOT [x] —` for negative constraints
- Use `// INVARIANT:` in tests for critical business rule assertions

## Where things go
- Business logic: src/services/
- Data access: src/repositories/ (or src/db/)
- Shared utilities: src/utils/ (pure functions only, no side effects)
- Types/interfaces: src/types/
- Configuration: src/config/ (never hardcoded)
- Tests: co-located with source OR tests/ (pick one, document here)

## What NOT to do
- [Anti-patterns specific to this project]
- [Patterns that were tried and abandoned]
```

---

## Step 4: ADR Setup

Create `docs/decisions/` with a `README.md`:

```markdown
# Architecture Decision Records

Decisions that shaped the architecture of this project.
Each ADR explains what was decided, why, and what was considered and rejected.

## Index
- [ADR-001: Project language choice](001-language-choice.md)
- [ADR-002: Database selection](002-database.md)
- [ADR-003: Auth strategy](003-auth-strategy.md)
```

Write your first 3 ADRs on day one — language, database, auth. These are the decisions
that AI agents will most often need to understand before touching your codebase.

---

## Step 5: The `.ai-context` Directory (Optional but Recommended)

For teams using AI agents heavily, create a `.ai-context/` directory at the root:

```
.ai-context/
├── README.md             ← "Read this before making any changes"
├── system-map.md         ← How the whole system fits together
├── danger-zones.md       ← The areas where wrong edits have high impact
└── onboarding.md         ← What an AI agent needs to know to work in this repo
```

`danger-zones.md` example:
```markdown
# Danger Zones

These are areas where incorrect changes cause serious problems.
Read the CONTEXT.md in each area before touching anything.

## Payment processing (src/payments/)
Incorrect changes can cause double-charges or failed charges.
- ALWAYS run: npm test -- payments before committing
- NEVER change retry logic without checking legal constraints in CONTEXT.md

## Auth (src/auth/)  
Incorrect changes can create security vulnerabilities.
- ALWAYS check the security model in ARCHITECTURE.md first
- The session TTL values are legal requirements, not preferences

## Database migrations (scripts/migrations/)
Irreversible in production. Cannot be rolled back safely.
- NEVER modify an existing migration file
- ALWAYS create a new migration for schema changes
```

---

## Daily Practice Checklist

When adding any new piece of code:

- [ ] Does the new file have a context header?
- [ ] Are non-obvious choices documented with a Decision Record?
- [ ] Are constraints that look like preferences documented with `DO NOT`?
- [ ] Are new tests named by behavior, not by function?
- [ ] Does the relevant `CONTEXT.md` need updating?
- [ ] Did I add any new business rules? → Document in `CONTEXT.md`
- [ ] Did I reject an approach? → Add to "tried and rejected" in `CONTEXT.md`
