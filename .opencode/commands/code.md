---
description: Implement SPEC.md task by task
agent: coder
---

Feature slug: $ARGUMENTS

## Input
Read: docs/specs/$ARGUMENTS/SPEC.md
Read: AGENTS.md for project conventions and standards

## Rules
- Implement ONE task at a time from the "Implementation Tasks" list
- Match naming, style, and structure of existing files
- After each file is created/modified, stop and wait for confirmation
- Never skip the Test Plan section — always implement the tests

## Process
1. Read docs/specs/$ARGUMENTS/SPEC.md
2. Announce which task you are starting: "## Task N: [description]"
3. Implement only that task
4. Show the complete file content
5. Stop and ask: "Task N complete. Proceed to Task N+1?"

Do not implement multiple tasks in a single response.
