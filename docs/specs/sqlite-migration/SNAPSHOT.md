# SNAPSHOT — sqlite-migration

## Feature

Replace JSON file-based persistence with SQLite database while maintaining backward compatibility with the existing CLI (Phase 1 of web migration).

---

## Decisions Made

- **SQLite over JSON**: Chosen for better performance, query capabilities, and foundation for future web API
- **Public API unchanged**: The `Database` class maintains identical methods (`load_tasks`, `save_tasks`, `load_milestones`, `save_milestones`) ensuring transparent migration for CLI users
- **Auto-migration on first run**: Detects existing JSON files and converts them automatically to SQLite format
- **Backup over deletion**: JSON files are moved to `data/json_backup/` instead of being deleted, preserving original data
- **In-memory SQLite for tests**: Uses `:memory:` path to ensure test isolation and avoid file system pollution
- **Idempotent migration**: Added `_data_exists_in_db()` check to prevent duplicate data if JSON files are re-added after migration
- **Transaction handling**: Migration wrapped in `BEGIN TRANSACTION` with rollback on failure to ensure atomicity
- **Resource management**: Added `close()` method and context manager support (`__enter__`/`__exit__`) for proper connection cleanup
- **ISO 8601 date storage**: SQLite stores dates as text strings in ISO format, converted back to `date`/`datetime` objects on load

---

## Files Created/Modified

| File | Purpose | Status |
|------|---------|--------|
| `phd_progress_tracker/utils/database.py` | Core persistence layer — refactored from JSON to SQLite | ✅ Modified |
| `tests/test_database.py` | Test suite for database operations — updated for SQLite | ✅ Modified |
| `phd_progress_tracker/models/task.py` | Task domain model — unchanged | ✅ Unchanged |
| `phd_progress_tracker/models/milestone.py` | Milestone domain model — unchanged | ✅ Unchanged |
| `phd_progress_tracker/cli/commands.py` | CLI commands — unchanged | ✅ Unchanged |

---

## Test Results

| Metric | Result |
|--------|--------|
| Total Tests | 78 passed |
| Database Tests | 15 passed |
| Overall Coverage | 95% |
| database.py Coverage | 87% (exception paths not tested) |
| flake8 | 0 errors |
| black | Compliant |

### Coverage Details

```
phd_progress_tracker/__init__.py          100%
phd_progress_tracker/cli/__init__.py      100%
phd_progress_tracker/cli/commands.py      100%
phd_progress_tracker/main.py               100%
phd_progress_tracker/models/__init__.py   100%
phd_progress_tracker/models/milestone.py  100%
phd_progress_tracker/models/task.py       100%
phd_progress_tracker/utils/__init__.py    100%
phd_progress_tracker/utils/database.py     87%
phd_progress_tracker/utils/date_helper.py 100%
```

### Known Limitations

- Exception handling paths in `database.py` (error conditions) are not covered by tests
- These represent ~13% of database.py lines that require artificial error injection to test

---

## Known Technical Debt

### 🟡 Medium Priority

- **Exception path coverage**: Lines 103-104, 115-117, 193-198, 232-233, 244-245, 292-293, and 304-305 in `database.py` handle error conditions but are not exercised by current tests. Would require mocking `sqlite3` errors or filesystem failures to test properly. Intentionally deferred as these represent edge cases that are difficult to reproduce reliably.

### 🟢 Low Priority

- **Advanced error recovery**: Could add retry logic for transient database errors (disk full, lock conflicts)
- **Connection pooling**: For file-based SQLite, could benefit from connection pooling in high-concurrency scenarios (not relevant for single-user CLI)

---

## State of the Application

O phd-progress-tracker é uma aplicação CLI em Python que permite aos estudantes de PhD gerenciar suas tarefas acadêmicas e marcos importantes da dissertação. A aplicação permite criar, editar e acompanhar tarefas com diferentes prioridades (Baixa, Média, Alta, Crítica) e status (A Fazer, Em Progresso, Concluída, Bloqueada), além de definir marcos importantes como qualificação e defesa. Com esta migração para SQLite, a camada de persistência foi atualizada de arquivos JSON para um banco de dados SQLite, mantendo total compatibilidade com a interface de linha de comando existente. Na primeira execução, dados JSON existentes são automaticamente migrados para o novo banco de dados, que é criado em `data/phd_tracker.db`, enquanto os arquivos originais são backupados em `data/json_backup/`. A aplicação agora está preparada para a próxima fase de migração para uma plataforma web com FastAPI como backend.

---

## Verification Commands

```bash
# Run all tests
poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing

# Run database-specific tests
poetry run pytest tests/test_database.py -v

# Verify linting
poetry run flake8 phd_progress_tracker/ tests/ --max-line-length=88
```

---

*Generated: 2026-02-25*
