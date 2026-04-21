# Negative Constraint Patterns

## Why Negative Constraints Are the #1 AI-First Tool

An AI agent reads code and infers intent from what IS there.
It cannot see what was decided NOT to do.
Negative constraints make invisible boundaries visible.

**The pattern:** `DO NOT [action] — [consequence if violated]`

---

## Pattern Library

### Business/Legal Constraints
```python
# DO NOT remove the rate limit on this endpoint — it's a contractual SLA
# with enterprise customers, not a technical choice. See contract #ENT-2024-047.

# DO NOT change the 30-day retention window — legal hold requirement.
# Shorter = compliance violation. Longer = storage cost SLA breach.

# DO NOT allow unauthenticated access to /api/admin even for health checks —
# penetration test finding 2024-Q2, see security-audit.md.
```

### Order/Sequence Constraints
```typescript
// DO NOT reorder these middleware — auth must run before rate-limit,
// which must run before logging. Logging captures auth context; 
// rate-limit needs auth identity. Wrong order = silent data loss.

// DO NOT parallelize these DB writes — they must be sequential.
// User record must exist before profile record (FK constraint).
// Promise.all() will cause intermittent failures under load.
```

### Performance/Scale Constraints
```go
// DO NOT add eager loading here — this query runs 10k/sec at peak.
// Each additional join costs ~40ms × 10k = 400s of DB time per second.
// Benchmark before any query change: see scripts/benchmark-query.sh

// DO NOT cache this value in memory — it's tenant-specific and
// the service runs 50 instances. Memory cache = stale data across instances.
// Use Redis (already wired in) or no cache.
```

### Integration/External Constraints
```python
# DO NOT change the field name 'legacy_user_id' — external partner API
# has hardcoded this field name. Renaming will silently break their pipeline.
# They cannot update their system. This is permanent. See partner-contracts/acme.md

# DO NOT increase timeout beyond 5s — upstream service has a 5s circuit breaker.
# Higher timeout on our side = we hold connections while they've already dropped us.
```

### Concurrency Constraints
```typescript
// DO NOT make this function async — it's called in a synchronous render path.
// Async here causes React to lose the event context, breaking form state.
// If async is needed, refactor the caller first.

// DO NOT remove the mutex here — this function is called from 3 goroutines.
// Looks unnecessary in tests (single-threaded), fails in production.
```

### "Obvious Fix" Traps
```python
# DO NOT simplify by removing the intermediate 'normalized_email' variable.
# The normalization (lowercase + strip) must happen BEFORE the uniqueness check.
# Direct comparison without normalization caused the login bug in issue #891.

# DO NOT replace this with a list comprehension — the for loop has a side effect
# on self._audit_log that must run for every item, including duplicates.
# A comprehension filters before iterating, which would miss audit entries.
```

---

## When to Write a Negative Constraint (Checklist)

Write one when:
- [ ] A limit exists for business or legal reasons (not technical preference)
- [ ] The "obvious refactor" would silently break something
- [ ] Order or sequence matters but isn't visible in the code
- [ ] A particular approach was deliberately rejected
- [ ] An integration partner has hardcoded assumptions about your code
- [ ] You've already fixed this bug once and it came back
- [ ] A performance optimization would cause correctness problems

---

## Anti-Patterns to Avoid

```python
# ❌ Too vague — doesn't explain consequence
# DO NOT modify this function

# ❌ Explains what, not why — AI already knows what it does
# DO NOT sort this list here (we sort later)

# ✅ Complete — action + consequence
# DO NOT sort here — downstream consumer depends on insertion order
# to determine event priority. Sorting breaks priority resolution in EventBus.
```

---

## Placement Rules

1. **Place at the exact line of the constraint** — not at the top of the file
2. **One constraint per comment** — don't bundle multiple DON'Ts in one block
3. **Link to evidence** when possible — issue numbers, contract refs, audit reports
4. **Date significant constraints** — `# DO NOT remove (added 2024-Q3, audit finding)`
