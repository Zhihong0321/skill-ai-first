---
name: ai-first-codebase
description: >
  Use this skill whenever the user wants to write, review, refactor, or structure code in a way that is optimized for AI agents to read, understand, edit, and maintain. Triggers include: "AI-first code", "write code for AI", "make code AI-readable", "context-aware code", "AI coding style", "optimize for AI agent", "add context to codebase", "write CONTEXT.md", "AI-optimized architecture", "code that AI can understand", "briefing for AI", "make code maintainable by AI", "set up AI-first project". Also trigger when the user is starting a new project and uses AI heavily, or when they're frustrated that their AI agent keeps making wrong edits. This skill redefines how code should be written when AI agents are primary contributors or maintainers.
---

# AI-First Codebase

## The Core Principle

> **Human-written code communicates to machines what to do.**  
> **AI-First code communicates to AI agents what to do, why it exists, and what must never change.**

A human senior developer holds the entire system in their mind. Intent, history, constraints — all implicit. An AI agent starts fresh every session with only what is written. The gap between what's written and what's meant is where AI agents break things.

**AI-First is the discipline of closing that gap — making implicit context explicit, at the exact point where decisions are made.**

---

## The 5 Layers of Code Meaning

Every codebase carries 5 layers. Normal code only preserves Layer 1. AI-First code preserves all 5.

| Layer | What it is | Normal code | AI-First code |
|---|---|---|---|
| **1. Mechanics** | What the code *does* | ✅ Always | ✅ Always |
| **2. Behavior** | What it *should* do | ⚠️ In tests | ✅ Tests + contracts |
| **3. Intent** | *Why* this approach | ❌ Rarely | ✅ Always |
| **4. History** | What was tried & rejected | ❌ Never | ✅ At decision points |
| **5. Domain** | The business reality it models | ❌ In people's heads | ✅ In CONTEXT files |

When an AI agent makes a confident, technically-correct, but wrong edit — it's missing Layer 3, 4, or 5.

---

## The 6 Practices

### Practice 1 — Negative Constraints
### Practice 2 — File Context Headers  
### Practice 3 — Inline Decision Records
### Practice 4 — Explicit Over Clever
### Practice 5 — CONTEXT.md per Domain
### Practice 6 — Tests as Living Spec

Read each practice below. When applying to a codebase, work through them in order.

---

## Practice 1: Negative Constraints

**The single highest-value thing you can write for an AI agent.**

Normal comments explain what code does. AI-First comments explain what must NOT happen and why.

```python
# ❌ Human-style (explains mechanics — AI already knows this)
# Loop through users and filter active ones

# ✅ AI-First (explains constraint + consequence)
# Filter to active users only.
# DO NOT include suspended users — they appear active in the DB
# but must not receive notifications (legal compliance, see #issue-412).
```

**The pattern:** `DO NOT [action] — [consequence if violated]`

**Write negative constraints when:**
- A limit exists for business/legal reasons (not technical ones)
- The "obvious improvement" would break something non-obvious
- A particular approach was deliberately rejected
- Order, timing, or sequence matters and isn't obvious from the code

**→ See `references/constraint-patterns.md` for a full pattern library with examples by language**

---

## Practice 2: File Context Headers

Every non-trivial file opens with a structured block that answers 4 questions:

```typescript
/**
 * WHAT:    [One sentence — what problem this file solves]
 * WHY:     [Why this file exists as a separate concern]
 * OWNS:    [What this file is responsible for]
 * NOT:     [What this file deliberately does NOT do — with pointer to what does]
 * DANGER:  [Rules that must not be violated, with reason]
 */
```

**Example:**
```typescript
/**
 * WHAT:    Payment retry scheduler
 * WHY:     Stripe webhooks unreliable in SEA region — this normalizes duplicates
 * OWNS:    Retry logic, backoff timing, failure escalation
 * NOT:     Does not process new payments (→ payment-processor.ts)
 *          Does not touch the ledger (→ ledger-service.ts)
 * DANGER:  3-retry cap is a legal requirement (2023-Q3 compliance audit).
 *          Do not increase without legal sign-off.
 */
```

**Rules:**
- Keep it under 10 lines
- The `NOT` field is as important as `OWNS` — it defines the boundary
- `DANGER` is for rules that look like implementation choices but are actually constraints
- Skip for files under ~30 lines with obvious purpose (utils, constants, index re-exports)

**→ See `templates/file-header.md` for templates by language (TS, Python, Go, Rust)**

---

## Practice 3: Inline Decision Records

When you make a non-obvious architectural choice, write a micro-ADR at the exact location of the decision.

```python
# DECISION: Redis sorted sets for this queue (not Postgres or SQS)
# Considered: PostgreSQL LISTEN/NOTIFY, AWS SQS, a cron job
# Rejected:
#   - PG: can't handle burst volume at peak load
#   - SQS: adds 200ms+ latency, unacceptable for this SLA
#   - Cron: 1-min minimum granularity — too coarse
# Revisit if: Redis becomes a bottleneck OR we go multi-region
```

**Write a Decision Record when:**
- You chose between multiple real options
- The chosen approach looks "wrong" without context
- The code will tempt future AI/humans to "fix" it
- A dependency or integration was chosen for non-obvious reasons

**The key field is "Revisit if"** — it tells the AI agent exactly when its job is to propose a change vs. preserve the current approach.

**→ See `references/decision-record-patterns.md` for templates and anti-patterns**

---

## Practice 4: Explicit Over Clever

AI agents are fast. Verbosity is free. Ambiguity is expensive.

```typescript
// ❌ Clever — compact but fragile to misread
const result = items?.filter(Boolean).reduce((a, b) => ({...a, [b.id]: b}), {}) ?? {}

// ✅ Explicit — each concern is a named step
const safeItems = items ?? [];
const validItems = safeItems.filter(item => item !== null && item !== undefined);
const result = validItems.reduce((acc, item) => {
  acc[item.id] = item;
  return acc;
}, {} as Record<string, Item>);
```

**Rules:**
- Name intermediate values — they document the transformation pipeline
- Avoid boolean flags as function parameters (`processUser(user, true, false)` → use named objects)
- Prefer early returns over nested conditionals
- One concept per line when intent matters
- Magic numbers always get a named constant with a comment

**This is not about being a worse programmer.** It's about writing code where AI agents can isolate, replace, and reason about each step independently.

**→ See `references/explicit-patterns.md` for before/after examples by pattern type**

---

## Practice 5: CONTEXT.md per Domain

The highest-leverage document in an AI-First codebase. Written *for AI agents*, not for humans.

Every major module, service, or domain gets a `CONTEXT.md` that an AI agent reads before touching anything in that area.

```markdown
# CONTEXT: [Module Name]

## What this module owns
[Bulleted list — specific, not vague]

## What it does NOT own
[Each item with a pointer: "→ handled by X"]

## Critical business rules
[Rules that look like implementation choices but are actually constraints]
[Each with: what the rule is, why it exists, consequence of violating]

## Known fragile areas
[Current weak spots, race conditions, tech debt — with workaround notes]

## What's been tried and rejected
[Past approaches that didn't work — so AI doesn't re-propose them]

## Dependency map
[What this module calls, what calls it — in plain language]

## Glossary
[Domain terms that mean something specific in this context]
```

**Placement:** `src/auth/CONTEXT.md`, `src/payments/CONTEXT.md`, etc. — lives next to the code it describes.

**Keep it updated.** A stale CONTEXT.md is worse than none — it actively misleads. Update it when business rules change, when you reject a new approach, when new fragile areas emerge.

**→ See `templates/CONTEXT-template.md` for the full template with guidance per section**

---

## Practice 6: Tests as Living Spec

Tests are the only form of documentation that breaks when it goes out of date. In AI-First codebases, they do double duty: verifying behavior AND briefing AI agents on what must be preserved.

```typescript
// ❌ Test that only verifies mechanics
it('processes payment', async () => {
  const result = await processPayment(mockPayload);
  expect(result.status).toBe('success');
});

// ✅ Test that preserves intent
it('rejects payment if user account is suspended — even with valid card', async () => {
  // Business rule: suspended accounts cannot transact regardless of payment validity
  // Violation would allow suspended users to bypass account restrictions via direct API
  const result = await processPayment({ ...mockPayload, user: suspendedUser });
  expect(result.status).toBe('rejected');
  expect(result.reason).toBe('account_suspended');
});
```

**Rules:**
- Test names describe *business behavior*, not implementation
- Include a one-line comment for non-obvious "why this must pass" tests
- Group tests by behavior domain, not by function name
- Add a `// INVARIANT:` comment on tests that encode critical business rules — these are the ones AI must never break

**→ See `references/test-as-spec.md` for naming patterns and invariant annotation guide**

---

## Applying This to an Existing Codebase

When retrofitting AI-First practices onto an existing project, work in this priority order:

1. **Write `CONTEXT.md` for the 3 most-edited modules first** — highest immediate ROI
2. **Add negative constraints to the 5 most "dangerous" functions** — the ones where a wrong AI edit would cause real damage
3. **Add file headers to modules AI touches most frequently**
4. **Retrofit Decision Records at the next opportunity** — when you're editing a file anyway, add the record for the non-obvious choice you're looking at
5. **Enforce explicit style going forward** — don't rewrite existing clever code unless you're already editing it

**Do not try to do everything at once.** Each CONTEXT.md written is immediate protection. Even one file header adds value. This is a practice you accumulate, not a migration you complete.

---

## Project Bootstrap (New Projects)

For new projects, set up the AI-First scaffold at day one:

```
project/
├── CONTEXT.md              ← Top-level: what this project is, what it's not
├── ARCHITECTURE.md         ← How the pieces fit together + key decisions
├── src/
│   ├── [module]/
│   │   ├── CONTEXT.md      ← Module-level context
│   │   └── *.ts / *.py
└── docs/
    └── decisions/          ← Major ADRs (the ones too big for inline)
```

**→ See `templates/project-bootstrap.md` for a full new project checklist**

---

## Quick Reference

| Situation | AI-First Practice |
|---|---|
| Writing a new function | Add negative constraints for non-obvious limits |
| Creating a new file | Add file context header (WHAT/WHY/OWNS/NOT/DANGER) |
| Making an architectural choice | Add inline Decision Record with "Revisit if" |
| Creating a new module | Create `CONTEXT.md` before writing any code |
| Writing tests | Name by behavior, annotate invariants |
| "Fixing" clever code | Make it explicit — name each step |
| AI made a wrong edit | Add the missing constraint/context where the edit happened |

---

## Reference Files

- `references/constraint-patterns.md` — Negative constraint library with examples
- `references/decision-record-patterns.md` — Decision record templates and anti-patterns  
- `references/explicit-patterns.md` — Before/after explicit vs clever code examples
- `references/test-as-spec.md` — Test naming and invariant annotation patterns
- `templates/file-header.md` — File header templates by language
- `templates/CONTEXT-template.md` — Full CONTEXT.md template with section guidance
- `templates/project-bootstrap.md` — New project AI-First setup checklist
