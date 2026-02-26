# Global Workflow Rules

## Spec-Driven Development Process
Every feature follows this pipeline:
1. /prd <slug>   → planner reads BRIEF.md → writes PRD.md
2. /spec <slug>  → planner reads PRD.md   → writes SPEC.md
3. /code <slug>  → coder reads SPEC.md    → implements
4. /test <slug>  → tester runs suite      → writes TEST_REPORT.md
5. /review <slug>→ reviewer audits code   → writes REVIEW_REPORT.md
6. /fix <slug>   → coder applies fixes    → updates TEST_REPORT.md
7. /snapshot <slug> → reviewer summarizes → writes SNAPSHOT.md

## Universal Rules
- Never commit directly to main — always work on a branch
- Branch naming: type/short-description-in-kebab-case
- Open a PR to merge — CI must pass before merging
- Always run tests before committing
- Every new function needs a test
- Commits follow: type(scope): description in English
- Branches follow: type/short-description-in-kebab-case

## Docs structure
- docs/specs/BRIEF.md        → human intent
- docs/specs/<slug>/PRD.md   → what to build
- docs/specs/<slug>/SPEC.md  → how to build it
- docs/specs/<slug>/TEST_REPORT.md
- docs/specs/<slug>/REVIEW_REPORT.md
- docs/specs/<slug>/SNAPSHOT.md
