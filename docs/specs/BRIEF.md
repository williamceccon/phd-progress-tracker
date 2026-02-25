BRIEF — SQLite Migration
Date: 2026-02-25
Slug: sqlite-migration

What I want
Replace the current local JSON storage with a SQLite database, keeping the CLI working exactly as it does today. After this feature is done, no JSON files should be used for data persistence.

Why it matters
The local JSON storage is a bottleneck for the next phase of the project, which involves building a REST API. SQLite is the natural migration step: it's still local, serverless, free, and fully compatible with the upcoming FastAPI layer.

Context
Current persistence layer lives in phd_progress_tracker/utils/database.py

Existing models: phd_progress_tracker/models/task.py and phd_progress_tracker/models/milestone.py

CLI commands are in phd_progress_tracker/cli/commands.py

Data is currently stored in local .json files (see utils/database.py for the exact structure)

Project uses Poetry and has 72 tests with 100% coverage

Constraints
No CLI command may change its visible behavior to the user

No new major dependencies without discussion (sqlite3 is Python built-in)

Coverage must remain at 100% after implementation

The CLI must continue working throughout and after the migration

Expected behavior
User runs any existing command → behavior is identical to today

Data persists between sessions in a SQLite database instead of JSON files

If JSON data already exists → a migration script converts it to SQLite automatically

If the SQLite database does not exist → it is created automatically on first run

Out of scope
REST API creation (next phase)

Any change to CLI commands or their output

Authentication or multi-user support

Remote hosting or cloud database

Success criteria
 All 72 tests passing with 100% coverage

 No JSON files used for persistence after migration

 Migration script (JSON → SQLite) working correctly

 CI/CD green after merge

 SQLite database auto-created if it does not exist

Open questions
What is the exact structure of the current JSON storage? The planner should inspect utils/database.py to map all fields before defining the SQL schema.