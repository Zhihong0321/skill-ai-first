# Model Routing

- repo: [repo name]
- purpose: route task types to the most capable AI model; record which model owns which area
- owner: human — AI agents may propose updates, human approves

---

## Task → Model Map

| Task type | Recommended model | Reason | Last reviewed |
|-----------|------------------|--------|--------------|
| Large file refactoring (>300 lines) | [model] | [why] | YYYY-MM-DD |
| New feature implementation | [model] | [why] | YYYY-MM-DD |
| Architecture planning | [model] | [why] | YYYY-MM-DD |
| Writing tests | [model] | [why] | YYYY-MM-DD |
| Cleanup and residual removal | [model] | [why] | YYYY-MM-DD |
| Codebase mapping and navigation | [model] | [why] | YYYY-MM-DD |
| Session handoff writing | any | low complexity | YYYY-MM-DD |
| Touching payment / auth / compliance | human-approved only | too high risk | YYYY-MM-DD |

---

## Models Active On This Codebase

| Model | Period active | Areas of ownership | Known tendencies |
|-------|--------------|-------------------|-----------------|
| [model] | YYYY-MM → YYYY-MM | [modules or areas] | [e.g., over-abstracts, strong at tests] |

---

## Do Not Use [model] For

- [task type]: [reason — regression history, known weakness, etc.]
