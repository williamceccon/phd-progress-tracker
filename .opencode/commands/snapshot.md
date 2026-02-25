---
description: Save a summary of current project state after a feature is complete
agent: reviewer
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Read docs/specs/$ARGUMENTS/PRD.md
2. Read docs/specs/$ARGUMENTS/SPEC.md
3. Read docs/specs/$ARGUMENTS/TEST_REPORT.md
4. Read docs/specs/$ARGUMENTS/REVIEW_REPORT.md
5. Read all source files modified in this feature
6. Write docs/specs/$ARGUMENTS/SNAPSHOT.md

## Output format for SNAPSHOT.md

### Feature
One sentence describing what was built.

### Decisions Made
Bullet list of design decisions and why.

### Files Created/Modified
| File | Purpose | Status |
|------|---------|--------|

### Test Results
Final coverage %, number of tests, known limitations.

### Known Technical Debt
Issues marked 🟡/🟢 intentionally deferred.

### State of the Application
Narrative paragraph in Portuguese: o que a aplicação faz hoje, end-to-end.
