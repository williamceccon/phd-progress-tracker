---
description: Review code and save report
agent: reviewer
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Run: `git diff main -- src/ tests/`
2. Read AGENTS.md for project conventions and standards
3. Write full analysis to docs/specs/$ARGUMENTS/REVIEW_REPORT.md

## Output format for REVIEW_REPORT.md

# Review Report — $ARGUMENTS
Date: [today]

## Issues Found
[numbered list with 🔴 high / 🟡 medium / 🟢 low severity]

## Verdict
✅ Approved — ready to merge
⚠️ Approved with suggestions — non-blocking issues found
❌ Needs changes — blocking issues must be fixed before merge
