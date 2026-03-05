BRIEF — Web Frontend Tests, Bug Fixes & Version 2.0 Polish
Date: 2026-03-04
Slug: web-tests-v2-polish

What I want
Fix the 404 bug on the milestones and tasks endpoints, add automated unit tests for the Next.js frontend, add usability tests to validate the full user flow, fix minor UI issues, and officially release the project as version 2.0 with updated documentation.

Why it matters
The frontend currently has a critical bug where creating tasks and milestones returns a 404 error, making the core functionality unusable. Beyond the bug fix, the frontend has zero automated tests — which is inconsistent with the high-quality standards established by the backend (95% coverage). Version 2.0 marks the architectural evolution from a pure CLI tool to a full local SaaS platform.

Context
Frontend is built with Next.js + Tailwind CSS, running on http://localhost:3000.

Backend is FastAPI, running on http://localhost:8000.

Known bug: POST http://localhost:8000/api/milestones and POST http://localhost:8000/api/tasks return 404. The planner must investigate whether the issue is in the FastAPI router prefix configuration in phd_progress_tracker/api/main.py, the URL base in web/lib/api.ts or web/.env.local, or a trailing slash mismatch between frontend and backend routes.

The Swagger UI at http://localhost:8000/docs should be used to verify the exact registered route paths and identify the mismatch.

There is a known text inconsistency in MilestoneList.tsx showing "dias para seguir" instead of "dias para frente".

The pyproject.toml and README.md still reflect an old version number.

Constraints
Use Vitest + React Testing Library for frontend unit tests.

Do not introduce E2E testing frameworks (Playwright/Cypress) in this phase.

Do not break existing Python backend tests (105 tests, 95% coverage).

Do not add new features — this phase is strictly bug fixing, testing, and polishing.

Expected behavior
Bug fix

User fills the task/milestone form and clicks "Criar" → data is saved successfully and appears in the list immediately.

No 404 errors in the browser console after fix.

Usability tests (manual test plan in a TEST_PLAN.md)

The planner should generate a structured manual usability test plan covering:

Dashboard: Loads correctly, stats update after creating/deleting tasks.

Tasks: Create, edit, mark as complete, delete — all flows work end-to-end.

Milestones: Create, edit, mark as achieved, delete — all flows work end-to-end.

Edge cases: Empty states (no tasks/milestones), form validation (required fields), error handling (API offline).

Responsive design: UI works correctly on mobile, tablet, and desktop viewports.

Frontend unit tests

At least 5 component tests covering: TaskForm, MilestoneForm, DashboardStats, StatusBadge, and Modal.

Running npm run test inside web/ executes all tests successfully.

Out of scope
E2E tests with Cypress or Playwright.

New features or UI changes beyond the known bug fixes.

Cloud deployment.

Increasing backend coverage beyond current 95%.

Success criteria
 POST /api/tasks and POST /api/milestones return 201 with no 404 errors.

 Creating a task or milestone via the UI saves and displays it correctly.

 npm run test passes with at least 5 frontend component tests.

 web/tests/TEST_PLAN.md created with full usability test checklist.

 Milestone text inconsistency fixed ("dias para seguir" → "dias para frente").

 web/README.md created with setup instructions.

 Root README.md updated to reflect the new v2.0 architecture (Backend + Frontend setup).

 pyproject.toml version bumped to 2.0.0.

 All 105 backend tests still passing with 95%+ coverage.

 CI/CD green after merge.

Open questions
Is the 404 caused by a prefix mismatch in main.py (routes registered as /tasks but frontend calls /api/tasks) or by a misconfigured base URL in the frontend (web/.env.local)? The planner must inspect both files and identify the root cause before proposing the fix.

Should the frontend coverage threshold be enforced via Vitest config (e.g., minimum 70%)? (Recommendation: yes, establish a minimum threshold from the start.)