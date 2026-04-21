# AI First Codebase Management

> *Built by AI. Maintained by AI. With discipline.*

A three-layer skill bundle for keeping large, AI-maintained codebases clean, navigable, and intentional — across long development cycles and multiple AI models.

---

## The Problem

AI coding agents are powerful. But over months and many sessions, they accumulate problems that no single session ever sees in full:

- files grow too large and mix too many responsibilities
- stale code and dead notes create confusion for future agents
- hard-won architectural decisions get reversed by agents with no memory of them
- a new model starts fresh with no knowledge of what was built or why
- the AI guesses at features it was never properly explained

This bundle addresses all of it — systematically, one task at a time.

---

## One Install, One Command

This bundle is meant to feel simple in practice:

- **One install**: install this whole repository as one bundle. Do not cherry-pick individual folders.
- **One command**: say `run ai-first-maintenance`.
- **Own memory**: on the first run, the bundle creates `.agents/ai-first-maintenance-log.md` in the maintained repo and keeps building on it across later sessions and weeks.

The internal specialist folders are implementation details of the bundle. For the user and the AI agent, the front door stays the same: install once, invoke one command, resume from the log next time.

---

## Quick Start

**Three steps. Under two minutes.**

---

### Step 1 — Install

Run from your **project root**:

**Simplest — git clone (no Python needed):**
```bash
git clone https://github.com/Zhihong0321/skill-ai-first.git .agents/skills/ai-first-maintenance-bundle
```

**Windows PowerShell:**
```powershell
$tmp = Join-Path $env:TEMP "install_ai_first.py"
Invoke-WebRequest https://raw.githubusercontent.com/Zhihong0321/skill-ai-first/main/scripts/install_from_github.py -OutFile $tmp
python $tmp --project-root .
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/Zhihong0321/skill-ai-first/main/scripts/install_from_github.py -o /tmp/install_ai_first.py
python3 /tmp/install_ai_first.py --project-root .
```

---

### Step 2 — Register with your AI

Pick the one that matches your setup:

**Cursor / Windsurf / Cline** — add one line to your rules file (`.cursorrules`, `.windsurfrules`, or `.clinerules`):
```
When the user says "run ai-first-maintenance", read and execute .agents/skills/ai-first-maintenance-bundle/ai-first-maintenance/SKILL.md
```

**Claude Projects / ChatGPT Custom Instructions** — paste into your project or system instructions:
```
When asked to "run ai-first-maintenance", read and follow .agents/skills/ai-first-maintenance-bundle/ai-first-maintenance/SKILL.md
```

**Any AI, no configuration** — say this at the start of any session:
```
Read .agents/skills/ai-first-maintenance-bundle/ai-first-maintenance/SKILL.md and run it.
```

---

### Step 3 — Run

Tell your AI:
```
run ai-first-maintenance
```

The first run creates `.agents/ai-first-maintenance-log.md` in your project and dispatches to the right specialist. Every session after, it reads the log and continues from where it left off.

---

## Built For

This bundle is optimized for five practical outcomes:

- **easy install, easy run**: install the bundle once, then trigger everything from `run ai-first-maintenance`
- **long-running AI maintenance authority**: the AI can work carefully across many sessions, one step at a time, without losing progress
- **file management discipline**: legacy files, stale notes, dead folders, and backup artifacts can be deleted, quarantined, or archived deliberately instead of piling up
- **robust progress memory**: the maintenance log and session handoff are treated as first-class operating files so later sessions can resume accurately
- **safer structural work**: risky cleanup, digestion, and optimization runs should happen on dedicated branches so they stay recoverable

---


## Three Layers

### Layer 1 — Maintenance Discipline
*Stop bad AI behavior before it compounds.*

A staged, single-task-per-run workflow that keeps the codebase clean, manageable, and structurally sound.

### Layer 2 — AI-First Operating System
*Make good AI behavior automatic across sessions and models.*

A persistent memory layer — session handoffs, decision logs, module contracts, blast radius maps, confidence signals — so every agent that touches the codebase starts informed rather than guessing.

### Layer 3 — AI-First Coding Style
*Write code that AI agents can read, trust, and change correctly.*

Coding practices that make implicit context explicit — inside the source files themselves — so AI agents never have to guess what must not change or why a decision was made.

---

## How It Works — The Front Desk Pattern

```
You say: "run ai-first-maintenance"
              │
              ▼
    ┌─────────────────────┐
    │     FRONT DESK      │  ai-first-maintenance/SKILL.md
    │                     │
    │  1. Read last-session.md   (was anything left unfinished?)
    │  2. Read maintenance log   (what stage are we at?)
    │  3. Run inventory scripts  (what needs attention?)
    │  4. Match dispatch table   (which specialist fits?)
    └──────────┬──────────┘
               │ dispatches to exactly ONE specialist
               ▼
    ┌─────────────────────┐
    │    SPECIALIST SKILL │  does one focused task
    │                     │  verifies the result
    │                     │  writes session handoff
    └─────────────────────┘
```

The Front Desk never performs specialist work. Specialists are invoked one at a time. Each run has one target, one deliverable, one log entry. This discipline is enforced at every level of the bundle.

---

## Layer 1 — Maintenance Skills

| Skill | What it does |
|-------|-------------|
| `ai-first-maintenance` | **Front Desk** — reads the situation, dispatches to one specialist only |
| `baseline-locker` | Confirms the current working state is safe before any changes |
| `codebase-mapper` | Builds a ranked maintenance map — reads at most 5 files per run |
| `file-digester` | Splits one oversized or overloaded file into focused modules |
| `residual-cleaner` | Removes one stale, dead, or confusing file or artifact |
| `architecture-optimizer` | Improves one structural problem — bounded to 3 files / 2 modules |
| `overhaul-planner` | Plans a full subsystem redesign when staged passes are not enough |

### Default Stage Order

```
baseline-locked → map-ready → digestion-ready → cleaning-ready → optimization-ready → overhaul-ready
```

Each stage is a gate. The Front Desk checks the log before moving forward. No stage is skipped silently.

---

## Layer 2 — AI-First Operating Skills

| Skill | Output file | What it does |
|-------|------------|-------------|
| `session-handoff` | `.agents/last-session.md` | Records what was left unfinished at end of every session |
| `decision-registrar` | `.agents/decisions.md` | Records WHY architectural choices were made |
| `context-navigator` | `.agents/nav.md` | Maps task types to required reading lists |
| `blast-radius-mapper` | `.agents/blast-radius.md` | Maps what breaks if a module is changed |
| `contract-writer` | inline `@ai-contract` headers | Defines scope boundaries inside each module |
| `ambiguity-register` | `.agents/ambiguities.md` | Tracks known unknowns — the do-not-guess list |
| `confidence-annotator` | inline `@ai-stable / @ai-uncertain / @ai-todo` | Tags code by how verified it is |

### The `.agents/` Memory Layer

Every agent that runs on a project reads these files first:

```
.agents/
├── ai-first-maintenance-log.md   ← staged maintenance history
├── last-session.md               ← what the last AI left unfinished
├── decisions.md                  ← WHY architectural choices were made
├── nav.md                        ← what to read for each task type
├── blast-radius.md               ← module impact map
└── ambiguities.md                ← known unknowns (do not resolve without human)
```

Ready-to-copy templates for all of these are in `templates/`.

---

## Layer 3 — AI-First Coding Style

| Practice | What it does |
|---------|-------------|
| Negative constraints | `DO NOT [action] — [consequence]` comments at the exact line of the constraint |
| File context headers | `WHAT / WHY / OWNS / NOT / DANGER` blocks at the top of every non-trivial file |
| Inline decision records | Micro-ADRs at the exact location of a non-obvious architectural choice |
| Explicit over clever | Named intermediate steps, early returns, named constants — code each AI step can audit independently |
| `CONTEXT.md` per domain | Module-level briefing file — business rules, known fragile areas, tried-and-rejected approaches, dependency map |
| Tests as living spec | Behavior-named tests with `// INVARIANT:` annotations on critical business rule assertions |

Templates and reference pattern libraries for all six practices are included in `ai-first-codebase/`.

---

## Anti-Over-Engineering Policy

Every structural skill in this bundle is guarded by `references/anti-overengineering.md`.

Before any digestion, optimization, or architecture work, the agent answers one test:

> **What concrete problem does this solve TODAY — not in the future, not hypothetically?**

Named patterns the policy explicitly guards against:

- **Abstraction injection** — new interface or layer with only one concrete user
- **Micro-splitting** — split produces files that must always be read together
- **Premature configurability** — config key with only one meaningful value
- **Utility accumulation** — helper function with exactly one caller
- **Rename creep** — renaming working things for "clarity" with no behavior change
- **Future-proofing drift** — hooks, plugins, extension points nobody asked for
- **Error infrastructure bloat** — custom error hierarchies before any caller needs them

The minimum viable change rule: *if the refactor touches more files than the problem itself does, the refactor is too large.*

---

## Scripts

Five audit and utility scripts — pure Python, no external dependencies:

| Script | Purpose |
|--------|---------|
| `inventory_large_files.py` | Rank files by size for digestion review (includes `.json`, `.yaml`, `.yml`) |
| `find_context_noise.py` | Detect stale/temp/legacy filename patterns — deduplicates noise dirs |
| `update_maintenance_log.py` | Initialize or append the maintenance log with validated fields |
| `find_missing_contracts.py` | List modules missing `@ai-contract` headers, sorted by size |
| `find_importers.py` | Find all files that reference a given module — for blast radius mapping |

---

## References

Policy files referenced by skills — never duplicated, always linked:

| Reference | Used by |
|----------|--------|
| `stage-selection.md` | Front Desk |
| `ai-friendly-code-shape.md` | file-digester |
| `soft-remove-policy.md` | residual-cleaner |
| `maintenance-log-policy.md` | All logging steps |
| `external-skill-intake.md` | When adopting outside skill patterns |
| `anti-overengineering.md` | file-digester, architecture-optimizer, contract-writer |
| `branch-safety.md` | Front Desk, risky action stages |

---

## Companion Bundle

This bundle integrates with **[RMINGI — Read My Intention](https://github.com/Zhihong0321/skill-read-my-intention)**.

RMINGI addresses the layer that even this bundle cannot solve on its own: **why each feature was built in the first place**.

> *When AI builds from short instructions, it guesses intent. Most of the time the guess is close enough. But over months and multiple models, those guesses compound — and the codebase drifts from its original purpose without anyone noticing.*

RMINGI reads the existing codebase, surfaces every guessed intention explicitly, and runs a sync dialogue with the human to confirm or correct each one. The output feeds directly into this bundle's `context-navigator` and `decision-registrar`.

---

## Installation

See [Quick Start](#quick-start) above for the fastest path.

**Requirements:** Python 3.8+ (only if not using git clone) · No external dependencies

**Custom install path:**
```bash
# Install to a specific skills directory
python install_from_github.py --skills-root /path/to/your/skills

# Install to an exact path
python install_from_github.py --target /exact/path/to/ai-first-maintenance-bundle
```

**Upgrade an existing install:**
```bash
python install_from_github.py --project-root . --force
```

**Installed layout:**
```
.agents/skills/ai-first-maintenance-bundle/
  ai-first-codebase/         ← Layer 3: write AI-first code
  ai-first-maintenance/      ← Front Desk — start here
  baseline-locker/
  ... (specialist skills)
  references/
  scripts/
  templates/
```

---

## Design Principles

- **One stage. One target. One deliverable.** Every run stops after one task.
- **Resume before you replace.** If a prior session left work unfinished, finish it first.
- **Log everything.** The maintenance log and session handoff are mandatory on every run.
- **Prefer reversible changes.** Soft-remove before delete. Plan before overhaul.
- **Quarantine before guessing.** If a legacy file or folder might still matter, move it out of the active path before deleting it permanently.
- **Branch before structural work.** Use a dedicated branch for cleanup, digestion, optimization, and overhaul passes.
- **Optimize for AI readability.** Not human preference, not theoretical perfection.
- **Read intention before touching anything.** What a feature does is in the code. Why it exists is not.
