BRIEF — Local Web Dashboard (Frontend)
Date: 2026-03-03
Slug: local-web-frontend

What I want
Create a modern, clean web frontend to consume the existing FastAPI backend. It should provide a user-friendly dashboard to manage PhD tasks and milestones, replacing the need to use the CLI while developing locally.

Why it matters
This is Phase 3 of the transition from a pure CLI tool to a SaaS platform. Having a visual dashboard allows for better task visualization, easier deadline management, and a more intuitive daily workflow for the user. It validates the REST API built in Phase 2 in a real-world scenario.

Context
The backend is a fully functional FastAPI app running on http://localhost:8000.

The API provides endpoints for Tasks (/api/tasks), Milestones (/api/milestones), and Dashboard stats (/api/dashboard).

Data is stored locally in SQLite (data/phd_tracker.db).

The Python backend and CLI must remain unchanged.

Constraints
Stack: Use Next.js (React) or SvelteKit (let the opencode planner decide based on simplicity and speed for this use case) paired with Tailwind CSS for styling.

Keep the frontend codebase in a new top-level directory (e.g., web/ or frontend/) to separate it from the Python backend.

Do not modify the existing Python backend or CLI code.

Must handle CORS correctly (the backend might need a small update to allow requests from the frontend's local port, usually localhost:3000 or 5173).

Expected behavior
Dashboard View: Shows the summary statistics (total, completed, pending, overdue) and a list of upcoming deadlines.

Tasks View: A list/board of all tasks where the user can create, edit, mark as complete, or delete tasks.

Milestones View: A section to track major PhD milestones, showing target dates and completion status.

Interaction: All actions in the UI must make HTTP requests to the FastAPI backend and update the UI accordingly.

Out of scope
User authentication or login screens (this is still for local, single-user use).

Complex drag-and-drop Kanban boards (keep it simple: lists or simple grids for now).

Cloud deployment or hosting setup.

Advanced charts or graphs (just display the data clearly).

Success criteria
 Frontend project successfully initializes and runs locally.

 UI successfully fetches and displays data from http://localhost:8000/api/dashboard.

 User can create, edit, and delete a task via the UI.

 User can create, edit, and delete a milestone via the UI.

 Backend tests still pass (no breaking changes to the API).

Open questions
Should the planner add a CORS middleware configuration to the FastAPI main.py to allow the frontend to communicate with it? (Highly likely yes, please include this in the spec).

Which frontend framework (Next.js vs SvelteKit) is better suited for this quick, single-page dashboard MVP?