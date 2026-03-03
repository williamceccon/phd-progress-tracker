# PRD — FastAPI Backend

## Overview

Create a REST API using FastAPI that exposes all existing CLI functionality as HTTP endpoints, using the existing SQLite database. After this feature, all CRUD operations for tasks and milestones must be accessible via HTTP requests while the CLI continues to work unchanged. This is Phase 2 of the web migration.

## Affected Files

| File | Change Type |
|------|-------------|
| `phd_progress_tracker/api/__init__.py` | New: API package init |
| `phd_progress_tracker/api/main.py` | New: FastAPI application entry point |
| `phd_progress_tracker/api/schemas.py` | New: Pydantic request/response schemas |
| `phd_progress_tracker/api/routes/tasks.py` | New: Task endpoints |
| `phd_progress_tracker/api/routes/milestones.py` | New: Milestone endpoints |
| `phd_progress_tracker/api/routes/dashboard.py` | New: Dashboard endpoint |
| `tests/test_api_tasks.py` | New: Task API tests |
| `tests/test_api_milestones.py` | New: Milestone API tests |
| `tests/test_api_dashboard.py` | New: Dashboard API tests |
| `pyproject.toml` | Update: add fastapi, uvicorn dependencies |
| `phd_progress_tracker/utils/database.py` | No change (reuse existing) |
| `phd_progress_tracker/cli/commands.py` | No change |
| `phd_progress_tracker/models/task.py` | No change |
| `phd_progress_tracker/models/milestone.py` | No change |

## Domain Concepts

- **Task**: id, title, description, deadline (date), status (enum), priority (enum), category (str), created_at (datetime), completed_at (datetime|null)
- **Milestone**: id, title, description, target_date (date), is_achieved (bool)
- **Dashboard stats**: total_tasks, completed_tasks, pending_tasks, overdue_tasks, upcoming_deadlines

## Implementation Plan

1. **Add dependencies**: Add `fastapi` and `uvicorn` to `pyproject.toml`
2. **Create Pydantic schemas** in `api/schemas.py` for request/response validation
3. **Create API router** in `api/routes/tasks.py` with CRUD endpoints for tasks
4. **Create API router** in `api/routes/milestones.py` with CRUD endpoints for milestones
5. **Create API router** in `api/routes/dashboard.py` for stats endpoint
6. **Create main FastAPI app** in `api/main.py` with OpenAPI configuration
7. **Write tests** for all endpoints using `TestClient` with in-memory database
8. **Run full test suite** to verify 95%+ coverage maintained

## API / Schema Design

### REST Endpoints

```
GET    /tasks              → List all tasks
POST   /tasks              → Create new task
GET    /tasks/{task_id}    → Get single task
PATCH  /tasks/{task_id}    → Update task (title, deadline, status, priority)
DELETE /tasks/{task_id}    → Delete task

GET    /milestones              → List all milestones
POST   /milestones              → Create new milestone
GET    /milestones/{milestone_id} → Get single milestone
PATCH  /milestones/{milestone_id} → Update milestone
DELETE /milestones/{milestone_id} → Delete milestone

GET    /dashboard          → Get summary statistics
GET    /docs               → Swagger UI (FastAPI built-in)
```

### Pydantic Schemas

```python
# Request schemas
class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: date
    category: str = "Geral"
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class MilestoneCreate(BaseModel):
    title: str
    description: str
    target_date: date

class MilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    is_achieved: Optional[bool] = None

# Response schemas
class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    deadline: date
    status: TaskStatus
    priority: TaskPriority
    category: str
    created_at: datetime
    completed_at: Optional[datetime]

class DashboardResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
```

### Database Integration

- Reuse existing `Database` class from `phd_progress_tracker.utils.database`
- Use dependency injection with `Depends()` for database instance
- Override `db_path` to use `:memory:` for test client

## Out of Scope

- Frontend/UI (next phase)
- Authentication or multi-user support
- Cloud deployment
- WebSockets or real-time updates
- File upload/download

## Success Criteria

- All existing 78 tests still passing
- API endpoints tested with pytest (new tests added)
- Coverage at 95% or higher
- Server starts with `poetry run uvicorn phd_progress_tracker.api.main:app --reload`
- Swagger UI accessible at http://localhost:8000/docs
- CLI behavior unchanged
- CI/CD green after merge

## Risks & Side Effects

- **Module structure**: Creating new `api/` directory must not conflict with existing imports
- **Database concurrency**: SQLite with FastAPI needs `check_same_thread=False` (already configured)
- **Date parsing**: Pydantic handles date validation; ensure format consistency between API and CLI

## Open Questions

- Should the API use Pydantic schemas separate from domain models, or reuse the existing models directly? → **Recommended: Use separate Pydantic schemas** for clear API contract and validation independence from domain logic.
