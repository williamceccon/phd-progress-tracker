---
description: Apply corrections from TEST_REPORT and REVIEW_REPORT
agent: coder
---

Feature slug: $ARGUMENTS

## Tasks
1. Read docs/specs/$ARGUMENTS/TEST_REPORT.md
2. Read docs/specs/$ARGUMENTS/REVIEW_REPORT.md
3. Fix ALL 🔴 high severity issues first, then 🟡 medium
4. Never change test logic to force passing — fix the source code
5. Read AGENTS.md to find the correct test command for this project
6. Run the full test suite after all fixes
7. Append to TEST_REPORT.md:
   ## Fix Round N — [date]
   [new test results]
