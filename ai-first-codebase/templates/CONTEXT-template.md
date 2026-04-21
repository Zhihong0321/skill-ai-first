# CONTEXT.md Template

Copy this into any module/domain directory. Fill in every section.
A missing section is not "not applicable" — it's a briefing gap.

---

```markdown
# CONTEXT: [Module/Domain Name]

> One sentence: what is this module's job in plain language?

---

## What this module owns

- [Specific responsibility 1]
- [Specific responsibility 2]
- [Be precise — vague ownership causes overlap and gaps]

## What it does NOT own

- [Concern 1] → handled by [other module/file]
- [Concern 2] → handled by [other module/file]
- [If a thing is "nobody's job", flag it as a gap]

---

## Critical business rules

These are constraints that look like implementation choices but are NOT.
Do not change these without understanding the reason.

| Rule | Reason | Consequence of violation |
|------|--------|--------------------------|
| [Rule 1] | [Why it exists] | [What breaks] |
| [Rule 2] | [Why it exists] | [What breaks] |

---

## Known fragile areas

Current weak spots, known bugs, or technical debt that AI agents must be aware of.

- **[Area name]**: [What's fragile and why]. Workaround: [current mitigation].
  Related: [issue/PR link if available]

- **[Area name]**: [What's fragile and why]. Workaround: [current mitigation].

---

## What's been tried and rejected

Approaches that were evaluated and rejected — so AI agents don't re-propose them.

- **[Approach]**: Tried [when/why]. Rejected because [specific reason].
  Revisit if: [condition that would change the calculus]

- **[Approach]**: Considered but not built. Rejected because [reason].

---

## Dependency map

What this module calls, and what calls it. Plain language — no need for a diagram.

**This module calls:**
- [Service/module] — for [what purpose]
- [Service/module] — for [what purpose]

**Called by:**
- [Service/module] — for [what purpose]
- [Service/module] — for [what purpose]

**External dependencies:**
- [Third-party service/library] — [what it does, any constraints on its use]

---

## Glossary

Domain terms that have specific meaning in this module's context.

| Term | Meaning here |
|------|-------------|
| [Term] | [What it means in this specific context, not the general definition] |
| [Term] | [Especially important if the term is overloaded across modules] |

---

## Related decisions

Links to ADRs or Decision Records that shaped this module.

- [ADR-001: Why we chose X](../docs/decisions/001-x.md)
- [ADR-007: Auth strategy](../docs/decisions/007-auth.md)
```

---

## Guidance Per Section

### "What it does NOT own" — the most underrated field
This is where scope creep hides. Being explicit about what this module doesn't do:
- Prevents AI agents from adding things that belong elsewhere
- Documents architectural decisions about separation of concerns
- Makes it easy to find where something should go when adding a feature

### "Critical business rules" — not technical rules
Technical rules (use this pattern, follow this convention) belong in SKILL.md or code comments.
CONTEXT.md business rules are things like:
- "Maximum 3 retry attempts — legal requirement, not a UX choice"
- "Free tier users cannot access this feature — business model boundary"
- "Audit log is append-only — compliance requirement"

### "What's been tried and rejected" — prevents groundhog day
This section stops AI agents (and humans) from proposing approaches you already know don't work.
The "Revisit if" condition is critical — it distinguishes "rejected forever" from "rejected for now."

### "Glossary" — prevents terminology drift
In AI-heavy development, the same concept gets different names across conversations.
Defining terms here ensures an AI agent uses the same vocabulary as the codebase.

---

## Keeping CONTEXT.md Fresh

Update CONTEXT.md when:
- A business rule changes
- You reject a new approach (add it to "tried and rejected")
- A new fragile area is discovered
- Module boundaries change (something moves in or out)
- A glossary term gets a new meaning

**A stale CONTEXT.md actively misleads AI agents.** It's worse than no CONTEXT.md.
Treat it like a test that must stay current.
