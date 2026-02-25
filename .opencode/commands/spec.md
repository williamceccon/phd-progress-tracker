---
description: Read PRD.md and generate SPEC.md with files and tasks
agent: planner
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Read docs/specs/$ARGUMENTS/PRD.md completely
2. Read all referenced source files in the codebase
3. Identify exactly what needs to be created or modified
4. Break the work into small, sequential tasks
5. Write the spec to docs/specs/$ARGUMENTS/SPEC.md

## Output — save to docs/specs/$ARGUMENTS/SPEC.md

### Files to Create
For each new file:
- Path
- Purpose (one sentence)
- Public interface: function/class signatures with type hints

### Files to Modify
For each existing file:
- Path
- What changes and why

### Implementation Tasks
Numbered list. Each task must be:
- Small enough to implement in one focused prompt
- Independent or clearly sequenced
- Testable

### Test Plan
- Which test file to create/modify
- List of test cases with expected behavior

Be precise. Avoid ambiguity. The coder agent will implement exactly this spec.
