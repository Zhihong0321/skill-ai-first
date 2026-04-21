# Decision Record Patterns

## Purpose

Inline Decision Records answer the question an AI agent will never think to ask:
**"What did they consider and reject before writing this?"**

Without this, an AI agent sees your Redis queue and "helpfully" refactors it to a
database queue — which you already tried, measured, and rejected three months ago.

---

## The Micro-ADR Format (Inline)

For decisions made at a specific line or function:

```
# DECISION: [What was decided — the chosen approach]
# Considered: [Other real options that were evaluated]
# Rejected because:
#   - [Option A]: [specific reason]
#   - [Option B]: [specific reason]
# Revisit if: [the condition that would make the rejected option worth trying again]
```

**The "Revisit if" field is the most important.** It tells an AI agent:
- When its job is to preserve this decision
- When its job is to flag that the condition has been met

---

## Examples by Decision Type

### Technology/Library Choice
```typescript
// DECISION: Using date-fns instead of moment.js or Day.js
// Considered: moment.js, Day.js, native Intl API
// Rejected because:
//   - moment.js: 67kb bundle, mutable API, officially in maintenance mode
//   - Day.js: API compatible with moment but has inconsistent plugin system
//   - Intl API: not enough timezone support for our locale requirements
// Revisit if: Intl.Temporal reaches Stage 4 and gets broad browser support
```

### Architecture Pattern
```python
# DECISION: Synchronous processing for this queue (not async workers)
# Considered: Celery workers, asyncio, separate microservice
# Rejected because:
#   - Celery: adds broker infra (Redis/RabbitMQ) we don't have yet
#   - asyncio: this code path has sync DB calls that can't be easily awaited
#   - Microservice: team too small to own another deployment unit right now
# Revisit if: queue depth regularly exceeds 1000 items OR team grows past 5 devs
```

### Data Model Choice
```sql
-- DECISION: Storing user preferences as JSON blob, not normalized rows
-- Considered: Separate preferences table with one row per preference
-- Rejected because: 
--   - Normalized: 50+ preference types × millions of users = table too wide for queries
--   - Preference schema changes weekly during current product iteration phase
--   - No need to query individual preferences in SQL — always fetched whole
-- Revisit if: We need to query/filter users BY a specific preference value
```

### External Service
```go
// DECISION: Twilio for SMS, not AWS SNS
// Considered: AWS SNS, Vonage, in-house via carrier direct
// Rejected because:
//   - SNS: no delivery receipts in Southeast Asia (our primary market)
//   - Vonage: 3x cost at our volume tier
//   - Carrier direct: requires individual contracts with 8+ carriers
// Revisit if: Monthly SMS volume exceeds $5k (SNS becomes cost-competitive at scale)
```

### "Don't Optimize Yet" Decisions
```python
# DECISION: Linear search here, not indexed lookup
# Considered: Dict/hashmap lookup, database index, caching layer
# Rejected because:
#   - Max 50 items in this list — linear search is O(n) where n≤50
#   - Adding a dict adds a sync requirement when source data updates
#   - Profiling shows this path runs <10/sec — not worth complexity
# Revisit if: List size can exceed 200 items OR this runs >1000/sec
```

---

## When to Write an Inline Decision Record

Write one when:
- [ ] You chose between two or more real alternatives
- [ ] The code looks like it's doing something suboptimal (but isn't)
- [ ] A dependency or library choice was non-obvious
- [ ] You deliberately kept something simple that could be more sophisticated
- [ ] You're rejecting what "best practice" would suggest, for valid reasons
- [ ] The previous implementation was replaced — why?

Skip it when:
- The choice is the only reasonable one (don't document why you used `len()` to get list length)
- The decision is well-covered in a `CONTEXT.md` file at the module level

---

## Module-Level ADRs (docs/decisions/)

For decisions too big for inline comments — ones that span multiple files or define the architecture — use full ADRs in `docs/decisions/`:

```markdown
# ADR-[number]: [Title]
**Date:** YYYY-MM-DD  
**Status:** Accepted | Superseded by ADR-X | Deprecated

## Context
[The situation that required a decision. What problem were you solving?]

## Decision
[What was decided. Be specific.]

## Alternatives Considered
[What else was evaluated and why it was rejected]

## Consequences
### Positive
[What this enables or improves]

### Negative / Trade-offs
[What this costs or constrains — be honest]

## Revisit Conditions
[When this decision should be re-evaluated]
```

**Naming:** `docs/decisions/001-database-choice.md`, `002-auth-strategy.md`  
**Reference from CONTEXT.md:** Always link to relevant ADRs from the module CONTEXT.md
