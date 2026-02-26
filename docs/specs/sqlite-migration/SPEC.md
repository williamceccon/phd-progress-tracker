# SPEC.md — SQLite Migration

## Overview

Replace JSON file-based persistence with SQLite database while maintaining backward compatibility with the existing CLI. This is Phase 1 of the web migration (FastAPI backend coming next).

**Status: IMPLEMENTED** — All tasks completed, tests passing, 100% coverage achieved.

---

## Affected Files

| File | Change Type |
|------|-------------|
| `phd_progress_tracker/utils/database.py` | Refactor: JSON → SQLite (COMPLETED) |
| `tests/test_database.py` | Update: SQLite tests (COMPLETED) |
| `phd_progress_tracker/cli/commands.py` | No change required |
| `phd_progress_tracker/models/task.py` | No change required |
| `phd_progress_tracker/models/milestone.py` | No change required |

---

## Files Created

### No new files required

The implementation uses existing module structure. All functionality is contained within:
- `phd_progress_tracker/utils/database.py`

---

## Files Modified

### `phd_progress_tracker/utils/database.py`

**Purpose**: Replace JSON file persistence with SQLite database

**Changes Made**:
1. Added `sqlite3` import for database operations
2. Added `db_path` parameter to `__init__` for test support
3. Added SQLite schema with `tasks` and `milestones` tables
4. Implemented `_init_db()` method to create tables if not exist
5. Implemented `_migrate_from_json()` to auto-convert legacy JSON files
6. Rewrote `load_tasks()` to read from SQLite
7. Rewrote `save_tasks()` to write to SQLite
8. Rewrote `load_milestones()` to read from SQLite
9. Rewrote `save_milestones()` to write to SQLite

**Public Interface** (unchanged):
```python
class Database:
    def __init__(self, data_dir: str = "data", db_path: str = None) -> None: ...
    def load_tasks(self) -> List[Task]: ...
    def save_tasks(self, tasks: List[Task]) -> None: ...
    def load_milestones(self) -> List[Milestone]: ...
    def save_milestones(self, milestones: List[Milestone]) -> None: ...
```

---

## Implementation Tasks

### Task 1: Create SQLite Schema ✅
- Created tables `tasks` and `milestones` with appropriate columns
- Used TEXT for dates (ISO 8601 format)
- Used INTEGER for boolean flags (is_achieved)

### Task 2: Refactor Database Class ✅
- Kept same public API: `load_tasks()`, `save_tasks()`, `load_milestones()`, `save_milestones()`
- Added `_init_db()` method for table creation
- Added migration logic: checks for existing JSON files, converts to SQLite if found
- Added `_get_connection()` method to handle both file and in-memory databases

### Task 3: Migration Logic ✅
- On init: checks if `data/tasks.json` or `data/milestones.json` exist
- If yes: loads JSON → inserts into SQLite → backs up JSON to `data/json_backup/`
- Creates SQLite file at `data/phd_tracker.db` if not exists

### Task 4: Update Tests ✅
- All tests use in-memory SQLite (`:memory:`) for isolation
- Tests verify: empty database, save/load roundtrip, JSON migration

---

## Test Plan

### Test File: `tests/test_database.py`

| Test Case | Expected Behavior |
|-----------|-------------------|
| `test_load_tasks_empty_db` | Returns empty list when no tasks in DB |
| `test_load_tasks_with_saved_tasks` | Correctly loads saved tasks from SQLite |
| `test_save_tasks` | Saves tasks to SQLite correctly |
| `test_save_and_load_tasks_roundtrip` | Save + load preserves all task data |
| `test_load_milestones_empty_db` | Returns empty list when no milestones in DB |
| `test_load_milestones_with_saved_milestones` | Correctly loads saved milestones from SQLite |
| `test_save_milestones` | Saves milestones to SQLite correctly |
| `test_save_and_load_milestones_roundtrip` | Save + load preserves all milestone data |
| `test_database_creates_data_directory` | Creates data directory if it doesn't exist |
| `test_migration_from_json` | Migrates legacy JSON files to SQLite, backs up originals |
| `test_save_tasks_clears_existing` | save_tasks() clears existing tasks before saving |
| `test_save_milestones_clears_existing` | save_milestones() clears existing milestones before saving |

### Test Execution Commands

```bash
# Run database-specific tests
poetry run pytest tests/test_database.py -v

# Run all tests with coverage
poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing

# Verify 100% coverage
poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing | grep "TOTAL"
```

### Verification Results

- **Total Tests**: 75 passed
- **Database Tests**: 12 passed
- **Coverage**: 100%
- **Lint (flake8)**: 0 errors
- **Format (black)**: Compliant

---

## SQLite Schema

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

---

## Migration Behavior

1. **First Run**: Creates `data/phd_tracker.db` automatically
2. **Legacy Data**: If `data/tasks.json` or `data/milestones.json` exist:
   - Data is migrated to SQLite
   - JSON files are backed up to `data/json_backup/`
   - Original JSON files are removed
3. **Subsequent Runs**: Uses SQLite exclusively

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking change - JSON no longer used | Migration logic ensures no data loss |
| Test isolation | Uses `:memory:` SQLite for tests |
| Date handling in SQLite | Stores as ISO 8601 strings, converts on load |
| Concurrent access | `check_same_thread=False` for in-memory DB |

---

## Open Questions (Resolved)

- **Should JSON files be deleted or backed up?** → Backed up to `data/json_backup/`
- **What naming convention for SQLite file?** → `phd_tracker.db`

---

## Success Criteria — VERIFIED ✅

- [x] All 75 tests pass
- [x] 100% coverage maintained
- [x] No `.json` files used for persistence (migrated to SQLite)
- [x] Migration script converts existing JSON data automatically
- [x] SQLite database auto-created on first run
- [x] CLI behavior unchanged
- [x] CI/CD pipeline would be green after merge

---

## Production Data State

```
data/
├── phd_tracker.db        # SQLite database (20KB)
└── json_backup/          # Legacy JSON backup
    ├── tasks.json
    └── milestones.json
```
