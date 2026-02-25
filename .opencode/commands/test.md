---
description: Create test plan based on SPEC.md
agent: tester
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Read docs/specs/$ARGUMENTS/SPEC.md to understand what was implemented
2. Read existing test files to understand testing patterns and conventions
3. Write TEST_REPORT.md with test plan (NOT execution results):

## Output format for TEST_REPORT.md

# Test Report — $ARGUMENTS
Date: [today]

## Test Plan

### Test Cases to Implement
| Test Case | File | Purpose | Expected Behavior |
|-----------|------|---------|-------------------|
| [from SPEC.md test plan] | [file] | [what it tests] | [expected result] |

### Test Execution Command (Deferred)
```bash
[command from AGENTS.md - NOT executed]
```

### Coverage Targets
- Target coverage: 100%
- Modules that need coverage: [list from SPEC.md]

### Known Test Dependencies
- Fixtures needed: [if any]
- Mock requirements: [if any]

## Notes
- Do NOT run tests — only create the plan
- Write what tests should exist, not the test results
