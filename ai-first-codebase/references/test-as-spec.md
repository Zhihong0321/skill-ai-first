# Tests as Living Spec

## The Dual Role of Tests in AI-First Codebases

In a normal codebase, tests verify behavior.
In an AI-First codebase, tests do two things:
1. Verify behavior (as usual)
2. **Brief AI agents on what must be preserved**

A well-named test with an intent comment is a constraint that breaks automatically
when violated. It's the highest-reliability form of negative constraint.

---

## Test Naming: Behavior Over Implementation

Test names should describe business behavior, not function calls.

```typescript
// ❌ Implementation-focused names
it('calls processPayment()', ...)
it('returns 200', ...)
it('throws error when null', ...)

// ✅ Behavior-focused names
it('rejects payment if user account is suspended — even with valid card', ...)
it('allows guest checkout without requiring account creation', ...)
it('sends confirmation email only after payment is confirmed, not on attempt', ...)
```

**The test name should be readable as a product requirement.**
If a non-coder read your test names, they should understand what the system guarantees.

---

## The INVARIANT Annotation

For tests that encode critical business rules — ones where a failing test means
a real-world consequence — add an `// INVARIANT:` comment:

```typescript
it('never charges a card more than once per order', async () => {
  // INVARIANT: duplicate charge prevention — financial/legal requirement
  // A retry bug caused double-charges in production (incident-2024-03-15).
  // This test must NEVER be disabled or modified to be less strict.
  
  const order = await createOrder(mockUser, mockCart);
  await processPayment(order);
  await processPayment(order); // second attempt — same order
  
  const charges = await stripe.getChargesForOrder(order.id);
  expect(charges).toHaveLength(1);
});
```

```python
def test_suspended_user_cannot_login():
    # INVARIANT: security boundary — suspended accounts must be completely locked out
    # Even if password is correct, suspended users must not receive a session token.
    # Relaxing this has compliance implications (SOC2 requirement AC-2).
    user = create_suspended_user(password="correct-password")
    response = client.post("/auth/login", json={
        "email": user.email, 
        "password": "correct-password"
    })
    assert response.status_code == 403
    assert "token" not in response.json()
```

---

## Grouping Tests by Business Domain

```typescript
// ❌ Grouped by function (implementation-centric)
describe('processPayment()', () => {
  it('works with valid card', ...)
  it('handles expired card', ...)
  it('handles insufficient funds', ...)
})

// ✅ Grouped by business scenario (behavior-centric)
describe('Payment Processing', () => {
  describe('when user is in good standing', () => {
    it('charges the card and creates an order record', ...)
    it('sends confirmation email within 30 seconds', ...)
  })
  
  describe('when payment fails', () => {
    it('does not create an order record if charge fails', ...)
    it('surfaces the specific decline reason to the user', ...)
    it('does not retry automatically — user must explicitly retry', ...)
    //  ^ INVARIANT: user-controlled retry is a deliberate UX decision (not a bug)
  })
  
  describe('account restrictions', () => {
    it('rejects payment for suspended accounts regardless of card validity', ...)
    it('rejects payment for accounts with outstanding disputes', ...)
  })
})
```

---

## Test Comments That Brief AI Agents

Add a comment when the "why" behind a test assertion isn't obvious:

```python
def test_email_normalized_before_uniqueness_check():
    # User@Example.COM and user@example.com must be treated as the same account.
    # This prevents duplicate account creation via case manipulation.
    # The normalization must happen in the model layer, not just the UI.
    create_user(email="User@Example.COM")
    
    with pytest.raises(DuplicateEmailError):
        create_user(email="user@example.com")
```

```typescript
it('preserves items in insertion order after refresh', async () => {
  // Order matters here — downstream invoice generation uses position[0] as
  // the primary line item for tax calculations. This is a billing system
  // constraint, not a UI preference. Do not sort or reorder.
  const cart = await createCart([itemC, itemA, itemB]);
  await refreshCart(cart.id);
  
  const refreshed = await getCart(cart.id);
  expect(refreshed.items.map(i => i.id)).toEqual([itemC.id, itemA.id, itemB.id]);
});
```

---

## The "Negative Behavior" Tests

Test what should NOT happen as much as what should:

```typescript
describe('Admin actions', () => {
  it('allows admin to view all user data', ...)
  
  // These test what must NOT happen — equally important
  it('does NOT allow admin to process refunds without finance approval', ...)
  it('does NOT log plain-text passwords even when user is admin', ...)
  it('does NOT expose other tenants data even to super-admins', ...)
})
```

---

## Quick Checklist for AI-First Tests

- [ ] Test names describe business behavior, not function names
- [ ] INVARIANT comment on any test encoding a legal/financial/security rule
- [ ] Tests grouped by business scenario, not by function
- [ ] "Should NOT" tests for critical negative behaviors
- [ ] Inline comment when the assertion would look overly strict without context
- [ ] No disabled/skipped tests without a comment explaining why and when to re-enable
