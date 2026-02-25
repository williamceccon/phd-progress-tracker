# phd-progress-tracker

## Project
PhD progress tracker — migrating from Typer CLI to SaaS Web platform.

## Stack
- **Now**: Python 3.13, Poetry, Typer, Rich, pytest
- **Next**: FastAPI (backend), Next.js + React (frontend), SQLite → PostgreSQL
- **CI/CD**: GitHub Actions (pytest + flake8 + black)
- **AI Tool**: OpenCode CLI

## Architecture
- `phd_progress_tracker/cli/commands.py` → CLI commands (Typer)
- `phd_progress_tracker/models/task.py`  → domain models
- `phd_progress_tracker/database.py`     → persistence layer
- `tests/`                               → mirrors source structure

## Code Conventions
- Commits: `type(scope): description` in English (Conventional Commits)
- Branches: `feature/`, `fix/`, `test/`, `docs/`
- Python style: black (formatter) + flake8 (linter)
- Always run `poetry run pytest` before committing
- Coverage must stay at 100% — add `# pragma: no cover` only for `if __name__ == "__main__"`

## Testing Rules
- Every new function must have a corresponding test
- Use in-memory SQLite for all database tests (never touch production DB)
- Test files mirror source: `tests/test_commands.py` for `cli/commands.py`

## Web Migration Guidelines (upcoming)
- FastAPI routes go in `api/` directory
- SQLAlchemy models replace current `models/`
- Alembic for database migrations
- Never break existing CLI while web layer is being built (parallel support)

## What NOT to do
- Never push directly to `main` — branch protection is enabled
- Always create a branch before starting any work: `type/short-description`
- Always open a PR to merge into main — CI must pass before merging
- Never skip tests
- Never add dependencies without updating `pyproject.toml`
- Never expose secrets in code or commits

## Commands
- **Run tests**: `poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing`
- **Lint**: `poetry run flake8 phd_progress_tracker/ tests/`
- **Format**: `poetry run black phd_progress_tracker/ tests/`
