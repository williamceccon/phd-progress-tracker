---
description: Run tests and save report
agent: tester
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Read AGENTS.md to find the correct test command for this project
2. Run the full test suite with coverage
3. Write the full output to docs/specs/$ARGUMENTS/TEST_REPORT.md

## Output format for TEST_REPORT.md

# Test Report — $ARGUMENTS
Date: [today]

## Results
[full test runner output]

## Verdict
- X passing / Y failing
- Coverage per module: 🔴 failing / 🟡 below 80% / 🟢 100%
