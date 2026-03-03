---
description: Run the full spec-driven development workflow (prd → spec → code → test → review → fix → test → snapshot)
agent: general
subtask: false
---

## Full Workflow Execution

Execute the complete spec-driven development framework for feature: **$ARGUMENTS**

### Step 1: PRD
Launch task with command: `/prd $ARGUMENTS`
- Creates docs/specs/$ARGUMENTS/PRD.md
- **Wait for completion, then ask user: "PRD created. Approve to continue to SPEC?"**

### Step 2: SPEC  
Launch task with command: `/spec $ARGUMENTS`
- Creates docs/specs/$ARGUMENTS/SPEC.md
- **Wait for completion, then ask user: "SPEC created. Approve to continue to CODE?"**

### Step 3: CODE
Launch task with command: `/code $ARGUMENTS`
- Implements the feature based on PRD.md and SPEC.md
- **Wait for completion**

### Step 4: TEST (Plan)
Launch task with command: `/test $ARGUMENTS`
- Creates TEST_REPORT.md with test plan
- **Wait for completion**

### Step 5: REVIEW (Plan)
Launch task with command: `/review $ARGUMENTS`
- Creates REVIEW_REPORT.md with review plan
- **Wait for completion**

### Step 6: FIX
Launch task with command: `/fix $ARGUMENTS`
- Runs tests, linter, formatter
- Fixes all high/medium severity issues
- **Wait for completion**

### Step 7: TEST (Verify)
Run: `poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing`
- Verifies all tests pass
- **Wait for completion**

### Step 8: SNAPSHOT
Launch task with command: `/snapshot $ARGUMENTS`
- Creates docs/specs/$ARGUMENTS/SNAPSHOT.md with final state
- **Workflow complete!**

## Output

All documentation saved to: docs/specs/$ARGUMENTS/

## Rules

1. WAIT for each step to complete before proceeding
2. If any step fails (tests fail, lint errors), STOP and report
3. After PRD and SPEC, always ask user for approval before /code
4. /test, /review, /fix run sequentially without approval (they're automated fixes)
