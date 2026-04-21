# File Header Templates

Use these at the top of every non-trivial source file.
Skip for: small utility files (<30 lines), index re-exports, simple constants files.

---

## TypeScript / JavaScript

```typescript
/**
 * WHAT:    [One sentence — what problem this file solves]
 * WHY:     [Why this is a separate file/module — what concern it isolates]
 * OWNS:    [What this file is responsible for — be specific]
 * NOT:     [What this file does NOT do — with pointer → where that lives]
 * DANGER:  [Rules that must not be violated, with reason]
 */
```

**Example:**
```typescript
/**
 * WHAT:    Tenant-aware database connection pool
 * WHY:     Each tenant requires an isolated connection with row-level security applied
 * OWNS:    Connection lifecycle, RLS context injection, connection health checks
 * NOT:     Does not handle migrations (→ scripts/migrate.ts)
 *          Does not manage tenant creation (→ services/tenant-service.ts)
 * DANGER:  RLS context MUST be set on every connection before queries run.
 *          A connection without RLS context exposes all tenant data.
 *          See: setTenantContext() — never bypass this.
 */
```

---

## Python

```python
"""
WHAT:    [One sentence — what problem this module solves]
WHY:     [Why this is a separate module — what concern it isolates]
OWNS:    [What this module is responsible for]
NOT:     [What this module does NOT do — with pointer to what does]
DANGER:  [Rules that must not be violated, with reason]
"""
```

**Example:**
```python
"""
WHAT:    Email notification queue and dispatch
WHY:     Decouples email sending from business logic to prevent transaction blocking
OWNS:    Queue management, retry logic, provider failover (SES → SendGrid)
NOT:     Does not template emails (→ templates/email/)
         Does not manage user notification preferences (→ services/user_prefs.py)
DANGER:  All emails must go through this queue — never call SES directly.
         Direct SES calls bypass the unsubscribe check and violate CAN-SPAM.
"""
```

---

## Go

```go
// Package [name] [one sentence — what this package does]
//
// WHAT:   [what problem this file/package solves]
// WHY:    [why this is a separate package]
// OWNS:   [responsibilities]
// NOT:    [what it doesn't do, with pointers]
// DANGER: [must-not-violate rules]
```

**Example:**
```go
// Package ratelimit provides per-tenant API rate limiting using sliding window algorithm.
//
// WHAT:   Per-tenant rate limiting with configurable windows and burst allowances
// WHY:    Isolates rate limiting logic from HTTP handlers for testability and reuse
// OWNS:   Window tracking, burst calculation, Redis state management
// NOT:    Does not authenticate tenants (→ pkg/auth)
//         Does not log rate limit events (caller's responsibility)
// DANGER: Redis key TTL must always exceed the window size.
//         Short TTL = counters reset mid-window = silent rate limit bypass.
```

---

## Rust

```rust
//! # [Module Name]
//!
//! WHAT:   [what this module solves]
//! WHY:    [why it's a separate module]
//! OWNS:   [responsibilities]
//! NOT:    [what it doesn't do, with pointers]
//! DANGER: [must-not-violate rules]
```

---

## Filling in DANGER

The DANGER field is where most value lives. Use it for:

- Rules that look like implementation choices but are actually constraints
- Security boundaries that must never be bypassed
- Performance rules that exist because of measured impact
- Integration contracts that external systems depend on
- Legal/compliance rules embedded in code

If you can't think of a DANGER for a file, write `none` — don't omit the field.
Its absence is the signal to an AI agent that this file has no hidden constraints.

---

## Minimal Version (when full header is overkill)

For medium-complexity files where only one thing really matters:

```typescript
// [One sentence what this does.]
// CONSTRAINT: [The one thing that must not change, with reason.]
```

Example:
```typescript
// Webhook signature validator for Stripe events.
// CONSTRAINT: Must validate signature BEFORE parsing payload body —
// parsing untrusted JSON before validation is a security vulnerability.
```
