# PRD — SQLite Migration

## Overview

Replace the current JSON file-based persistence layer with SQLite database while maintaining complete backward compatibility with the existing CLI. This is Phase 1 of the web migration (FastAPI backend coming next).

## Affected Files

| File | Change Type |
|------|-------------|
| `phd_progress_tracker/utils/database.py` | Refactor: JSON → SQLite |
| `tests/test_database.py` | Update: match new SQLite implementation |
| `phd_progress_tracker/cli/commands.py` | No change (interface unchanged) |
| `phd_progress_tracker/models/task.py` | No change (domain model unchanged) |
| `phd_progress_tracker/models/milestone.py` | No change (domain model unchanged) |

## Domain Concepts

- **Task**: id, title, description, deadline (date), status (enum), priority (enum), category (str), created_at (datetime), completed_at (datetime|null)
- **Milestone**: id, title, description, target_date (date), is_achieved (bool)
- **Database**: persistence layer abstracting storage (currently JSON, moving to SQLite)

## Implementation Plan

1. **Create SQLite schema** in `database.py` with two tables: `tasks` and `milestones`
2. **Refactor `Database` class**:
   - Keep same public API: `load_tasks()`, `save_tasks()`, `load_milestones()`, `save_milestones()`
   - Add `_init_db()` method to create tables if not exist
   - Add migration logic: check for existing JSON files, convert to SQLite if found
3. **Update tests** in `test_database.py` to work with SQLite (use in-memory DB for tests)
4. **Run full test suite** to verify 100% coverage maintained

## API / Schema Design

### SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    deadline TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS milestones (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    target_date TEXT NOT NULL,
    is_achieved INTEGER NOT NULL
);
```

### Database Class API (unchanged)

```python
class Database:
    def __init__(self, data_dir: str = "data"): ...
    def load_tasks(self) -> List[Task]: ...
    def save_tasks(self, tasks: List[Task]) -> None: ...
    def load_milestones(self) -> List[Milestone]: ...
    def save_milestones(self, milestones: List[Milestone]) -> None: ...
```

### Migration Logic

- On init: check if `data/tasks.json` or `data/milestones.json` exist
- If yes: load JSON → insert into SQLite → delete JSON files (optional: backup first)
- Create SQLite file at `data/phd_tracker.db` if not exists

## Risks & Side Effects

- **Breaking change**: JSON files are no longer used (but migration ensures no data loss)
- **Test isolation**: Must use in-memory SQLite (`":memory:"`) for tests to avoid polluting each test
- **Date handling**: SQLite doesn't have native date/datetime—store as ISO 8601 strings

## Out of Scope

- REST API / FastAPI layer (next phase)
- CLI command modifications
- Multi-user support or authentication
- Cloud/remote database hosting

## Success Criteria

- All 72+ tests pass with 100% coverage
- No `.json` files used for persistence after migration
- Migration script converts existing JSON data automatically
- SQLite database auto-created on first run
- CLI behavior unchanged (verified by existing tests)
- CI/CD pipeline green after merge

## Open Questions

- Should JSON files be deleted or backed up after migration? (Recommend: backup to `data/json_backup/`)
- What naming convention for SQLite file? (Recommend: `phd_tracker.db`)
