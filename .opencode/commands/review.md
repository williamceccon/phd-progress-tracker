---
description: Create code review plan based on SPEC.md
agent: reviewer
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Read docs/specs/$ARGUMENTS/SPEC.md to understand what was implemented
2. Read source files that were modified (listed in SPEC.md)
3. Read AGENTS.md for project conventions and standards
4. Write REVIEW_REPORT.md with review plan (NOT execution):

## Output format for REVIEW_REPORT.md

# Review Report — $ARGUMENTS
Date: [today]

## Review Plan

### Files to Review
| File | Purpose | Key Areas to Check |
|------|---------|-------------------|
| [from SPEC.md] | [what it does] | [security, style, etc.] |

### Areas to Review
- Code style (follows project conventions)
- Type hints and docstrings
- Error handling
- Security (SQL injection, etc.)
- Edge cases
- Magic numbers or hardcoded values

### Verification Commands (Deferred - NOT executed)
```bash
# Lint command from AGENTS.md
poetry run flake8 ...

# Format check from AGENTS.md
poetry run black --check ...

# Type check (if applicable)
poetry run mypy ...
```

### Potential Issues to Look For
- [List of common issues based on the feature type]

## Notes
- Do NOT run commands — only create the review plan
- Write what should be checked, not the actual results
