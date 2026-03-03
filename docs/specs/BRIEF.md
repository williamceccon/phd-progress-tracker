BRIEF — FastAPI Backend
Date: 2026-02-25
Slug: fastapi-backend

What I want
Create a REST API using FastAPI that exposes all existing CLI functionality as HTTP endpoints, using the SQLite database already implemented. After this feature is done, all CRUD operations for tasks and milestones must be accessible via HTTP requests, while the CLI continues to work normally.

Why it matters
This is Phase 2 of the web migration. The FastAPI backend is the bridge between the current CLI and the future web UI. Without it, there is no way to build a frontend that reads and writes data.

Context
Persistence layer: phd_progress_tracker/utils/database.py (SQLite, already migrated)

Domain models: phd_progress_tracker/models/task.py and phd_progress_tracker/models/milestone.py

CLI commands in phd_progress_tracker/cli/commands.py — must remain untouched

Existing enums: status and priority on Task model

Database file: data/phd_tracker.db

Project uses Poetry, Python 3.12, 78 tests with 95% coverage

Constraints
CLI must continue working after this feature

Coverage must remain at 95% or higher

No breaking changes to existing models or database layer

FastAPI and Uvicorn are the only new dependencies allowed

API must run locally on http://localhost:8000

Expected behavior
GET /tasks → returns list of all tasks

POST /tasks → creates a new task, returns created task

PATCH /tasks/{id} → updates a task (title, deadline, status, priority)

DELETE /tasks/{id} → deletes a task

GET /milestones → returns list of all milestones

POST /milestones → creates a new milestone

PATCH /milestones/{id} → updates a milestone

DELETE /milestones/{id} → deletes a milestone

GET /dashboard → returns summary stats (total tasks, completed, pending, upcoming deadlines)

GET /docs → FastAPI auto-generated Swagger UI accessible in browser

Out of scope
Frontend/UI (next phase)

Authentication or multi-user support

Cloud deployment

WebSockets or real-time updates

Success criteria
 All existing 78 tests still passing

 API endpoints tested with pytest (new tests added)

 Coverage at 95% or higher

 Server starts with poetry run uvicorn phd_progress_tracker.api.main:app --reload

 Swagger UI accessible at http://localhost:8000/docs

 CLI behavior unchanged

 CI/CD green after merge

Open questions
Should the API use Pydantic schemas separate from the domain models, or reuse the existing models directly? The planner should evaluate and recommend the best approach.    