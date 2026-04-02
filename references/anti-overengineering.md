# Anti-Over-Engineering Policy

Over-engineering is the most common quality failure in AI-maintained codebases.
It does not look like a bug. It looks like improvement. That is what makes it dangerous.

Read this reference before any digestion, optimization, or architecture work.

---

## The Core Test

Before adding any abstraction, layer, or structural change, answer this:

> **What concrete problem does this solve TODAY — not in the future, not hypothetically?**

If the answer contains "it would be cleaner", "in the future we might", or "it's better practice",
**do not make the change.**

---

## Patterns That Signal Over-Engineering

Stop and reconsider if any of these are true:

### Abstraction with no second user
- new interface, abstract class, or base class with exactly one implementor
- new service layer wrapping a module that only one caller uses
- new factory or builder pattern with one product type
→ **do not add it** — extract only when the second concrete use actually exists

### Splits that must be read together
- file digestion produces 4+ new files that always need to be loaded as a group
- no single new file can be understood without reading the others
→ **the split is wrong** — find a different boundary, or do not split yet

### Configurability that serves no real variant
- adding a config key, feature flag, or environment variable with only one meaningful value
- making behavior configurable "in case someone needs to change it"
→ **hardcode it** — extract the constant when the second value appears

### Utility functions with one caller
- new shared helper used in exactly one place
- generic logic extracted "for reuse" with no existing second caller
→ **leave it inline** — extract when the second caller appears

### Rename without behavior change
- renaming functions, files, or variables to "better" names
- "improving" naming across multiple files in one pass
→ **do not rename unless the current name actively causes confusion** — rename noise fills diffs and loses history with no value

### Future-proofing infrastructure
- adding plugin systems, hook points, event buses, or extension interfaces not yet used
- adding middleware layers "for future flexibility"
→ **do not build for imagined futures** — build for the current problem only

### Error infrastructure bloat
- creating custom error class hierarchies for simple operations
- wrapping plain errors in typed error objects before any caller needs to distinguish them
→ **throw or return plain errors** until a concrete need for differentiation exists

### Comment over-documentation
- replacing readable 3-line logic with 10 lines of prose comments explaining it
- adding JSDoc / docstrings to trivially obvious functions
→ **write clearer code instead** — comments that explain intent are good; comments that narrate code are noise

---

## The Minimum Viable Change Rule

For any structural change, ask:

> What is the **smallest** change that solves the actual problem?

If a refactor touches more files than the problem itself does, the refactor is too large.
If a split adds more files than the original had responsibility boundaries, the split is too aggressive.

---

## What Good Simplification Looks Like

Good structural work:
- **removes** a layer that adds complexity without adding clarity
- **merges** two related files that were split for no architectural reason
- **deletes** utility functions that were added speculatively and are used once
- **inlines** configuration that was made flexible before flexibility was needed
- **reduces** the number of concepts a future AI agent needs to hold in context

Over-engineering adds. Good maintenance often **removes**.

---

## When To Reference This File

Read this before:
- any `file-digester` run that produces more than 2 new files
- any `architecture-optimizer` run that introduces a new pattern or layer
- any `contract-writer` run — contracts should describe what IS, not what COULD be
- any run where you are tempted to add something that does not exist yet
