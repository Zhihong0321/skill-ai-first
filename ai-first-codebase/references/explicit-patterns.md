# Explicit Over Clever — Pattern Reference

## The Principle

AI agents are fast. Verbosity costs nothing meaningful.
Ambiguity costs wrong edits, missed edge cases, and silent bugs.

**Explicit code = code where each step has a name, a purpose, and is independently auditable.**

This is not dumbed-down code. It's code where intent is visible at every step.

---

## Pattern: Name Your Transformations

```typescript
// ❌ Clever chain — what does each step do? What if one fails?
const result = data?.users
  ?.filter(u => u.active && !u.deleted)
  .map(u => ({ ...u, displayName: `${u.first} ${u.last}` }))
  .sort((a, b) => a.displayName.localeCompare(b.displayName))
  ?? [];

// ✅ Named steps — each is auditable, testable, replaceable
const safeUsers = data?.users ?? [];
const eligibleUsers = safeUsers.filter(u => u.active && !u.deleted);
const usersWithDisplayName = eligibleUsers.map(u => ({
  ...u,
  displayName: `${u.first} ${u.last}`
}));
const sortedUsers = usersWithDisplayName.sort(
  (a, b) => a.displayName.localeCompare(b.displayName)
);
```

Why this matters for AI: If a bug appears in the sorted output, an AI agent can
isolate exactly which step to inspect. In the chained version, it might rewrite the
whole chain when only the sort comparator needs changing.

---

## Pattern: Named Parameters Over Positional Booleans

```python
# ❌ What does True, False, True mean?
result = process_user(user, True, False, True)

# ✅ Intent is readable without looking at the function signature
result = process_user(
    user,
    send_welcome_email=True,
    require_verification=False,
    log_activity=True
)
```

---

## Pattern: Early Returns Over Deep Nesting

```typescript
// ❌ Deeply nested — AI must track all conditions simultaneously
function getUserPermission(user, resource) {
  if (user) {
    if (user.isActive) {
      if (!user.isSuspended) {
        if (resource.isPublic || user.hasAccess(resource)) {
          return 'granted';
        } else {
          return 'denied';
        }
      } else {
        return 'suspended';
      }
    } else {
      return 'inactive';
    }
  } else {
    return 'unauthenticated';
  }
}

// ✅ Early returns — each failure case is isolated and clear
function getUserPermission(user, resource) {
  if (!user) return 'unauthenticated';
  if (!user.isActive) return 'inactive';
  if (user.isSuspended) return 'suspended';
  if (!resource.isPublic && !user.hasAccess(resource)) return 'denied';
  return 'granted';
}
```

---

## Pattern: Named Constants for Magic Values

```python
# ❌ Where do these numbers come from? Are they related?
if retry_count >= 3:
    wait_time = 300
    
# ✅ The name carries the intent — and the DECISION of why 3 and 300
MAX_PAYMENT_RETRIES = 3          # Legal requirement: max 3 attempts per 24h window
RETRY_LOCKOUT_SECONDS = 300      # 5-minute cooling period between retry windows

if retry_count >= MAX_PAYMENT_RETRIES:
    wait_time = RETRY_LOCKOUT_SECONDS
```

---

## Pattern: Explicit Error Handling

```typescript
// ❌ Swallowed errors — AI can't see what might go wrong
async function fetchUser(id: string) {
  try {
    return await db.users.findById(id);
  } catch {
    return null;
  }
}

// ✅ Explicit failure modes — AI knows what errors are expected vs unexpected
async function fetchUser(id: string): Promise<User | UserNotFoundError> {
  try {
    const user = await db.users.findById(id);
    if (!user) return new UserNotFoundError(id);
    return user;
  } catch (err) {
    if (err instanceof DatabaseConnectionError) {
      // Expected: DB timeout — caller should retry
      throw err;
    }
    // Unexpected: log and surface
    logger.error('Unexpected error fetching user', { id, err });
    throw err;
  }
}
```

---

## Pattern: Typed Over Stringly-Typed

```python
# ❌ String literals everywhere — AI can't validate or trace these
def set_user_status(user_id, status):  # status is "active", "inactive", "suspended"???
    db.users.update(user_id, {"status": status})

# ✅ Explicit type — AI knows exactly what values are valid
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive" 
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

def set_user_status(user_id: str, status: UserStatus) -> None:
    db.users.update(user_id, {"status": status.value})
```

---

## What This Is NOT

- Not about writing longer code for its own sake
- Not about avoiding all abstractions
- Not about avoiding functional programming

**Keep abstractions when they're genuinely reusable and well-named.**  
Make things explicit when the transformation, decision, or constraint matters.

The test: **Can an AI agent, reading this code without any other context, correctly identify what to change and what to preserve?**
