---
name: git-commit
description: Commit message and branch naming standards for this project
---

## Commit format
type(scope): short description in English

## Valid types and scopes

| Type       | Scope                                              |
|------------|----------------------------------------------------|
| feat       | cli, api, web, db, models, auth, export, notif     |
| fix        | cli, api, web, db, models, auth, config            |
| test       | cli, api, db, models, auth, export                 |
| docs       | readme, agents, skills, specs, changelog           |
| refactor   | cli, db, models, api, config                       |
| chore      | deps, ci, config, hooks                            |

## Branch naming
type/short-description-in-kebab-case

## Valid examples
feat(db): migrate persistence layer to SQLite
feat(cli): add export command with JSON and CSV support
fix(db): fix in-memory isolation between test sessions
test(cli): cover add-task edge cases with empty input
docs(readme): add Codecov badge and setup instructions
refactor(models): extract Task validation into separate method
chore(ci): add Codecov upload step to GitHub Actions workflow
chore(deps): add alembic and sqlalchemy to pyproject.toml
