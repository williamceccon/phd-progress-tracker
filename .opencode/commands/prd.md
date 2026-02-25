---
description: Research codebase and generate PRD.md for the current session
agent: planner
subtask: true
---

Feature slug: $ARGUMENTS

## Tasks
1. Read docs/specs/BRIEF.md — this is the human intent for this session
2. Read all relevant project files: src/, tests/, docs/, pyproject.toml, AGENTS.md
3. Identify which modules, patterns and conventions already exist
4. Create the folder docs/specs/$ARGUMENTS/ if it does not exist
5. Write the PRD to docs/specs/$ARGUMENTS/PRD.md

## Output — save to docs/specs/$ARGUMENTS/PRD.md

### Context
- What phase of the project this belongs to
- Which existing files/modules are affected

### Goal
- One sentence: what this session must deliver

### Domain Concepts
- Key domain entities and terms involved in this feature

### Functional Requirements
- Bullet list of what must work (no implementation details)

### Non-Functional Requirements
- Performance, test coverage, security, and any project-specific constraints from AGENTS.md

### Out of Scope
- What will NOT be done in this session

### Success Criteria
- How to verify this session was successful (tests passing, endpoints responding, etc.)

Be concise. Max 1 page.
