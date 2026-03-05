# PRD — Web Tests, Bug Fixes & Version 2.0 Polish

## Overview

This session addresses critical bugs in the web frontend, introduces automated testing for the React components, fixes minor UI issues, and formally releases the project as version 2.0. The work represents the final polish phase before the official v2.0 release, marking the transition from a CLI-only tool to a full local SaaS platform.

## Context

### Project Phase

This is the **v2.0 Release Phase** — the culmination of the web migration effort. The project has evolved from a Python CLI tool (Typer) to a full-stack application with FastAPI backend and Next.js frontend.

### Affected Modules

| Layer | File | Change Type |
|-------|------|-------------|
| Backend | `phd_progress_tracker/api/main.py` | No change needed |
| Backend | `phd_progress_tracker/api/routes/tasks.py` | No change needed |
| Backend | `phd_progress_tracker/api/routes/milestones.py` | No change needed |
| Frontend | `web/lib/api.ts` | Fix: Remove `/api` prefix from endpoints |
| Frontend | `web/components/MilestoneList.tsx` | Fix: Text correction |
| Config | `pyproject.toml` | Update version to 2.0.0 |
| Config | `web/package.json` | Update version + add test dependencies |
| Docs | `README.md` | Update for v2.0 architecture |
| New | `web/README.md` | Create frontend setup guide |
| New | `web/tests/TEST_PLAN.md` | Create usability test plan |

## Goal

Fix the 404 bug preventing task/milestone creation, add at least 5 frontend component unit tests using Vitest, fix the "dias para seguir" text inconsistency, update version to 2.0.0, and release the polished v2.0 platform.

## Root Cause Analysis: 404 Bug

### The Problem

POST requests to create tasks and milestones return HTTP 404 from the backend.

### Investigation Results

| Component | Route Configuration | Frontend Call |
|-----------|---------------------|---------------|
| Tasks | `/tasks` (no prefix) | `/api/tasks` |
| Milestones | `/milestones` (no prefix) | `/api/milestones` |
| Dashboard | `/dashboard` (no prefix) | `/api/dashboard` |

**Root Cause**: The FastAPI routers are registered with prefixes `/tasks`, `/milestones`, and `/dashboard` (defined in `phd_progress_tracker/api/routes/tasks.py`, `milestones.py`, and `dashboard.py`). However, the frontend API client in `web/lib/api.ts` calls these endpoints with an `/api` prefix.

### Recommended Fix

Update `web/lib/api.ts` to remove the `/api` prefix from all endpoint paths, making them consistent with the backend router configuration:

- `/api/dashboard` → `/dashboard`
- `/api/tasks` → `/tasks`
- `/api/tasks/{id}` → `/tasks/{id}`
- `/api/milestones` → `/milestones`
- `/api/milestones/{id}` → `/milestones/{id}`

This is the minimal change — modifying the frontend is safer than modifying the backend routes, as the backend routes are already tested and working (verified via Swagger UI at `/docs`).

## Domain Concepts

### Backend Entities

- **Task**: `id`, `title`, `description`, `deadline`, `status`, `priority`, `category`, `created_at`, `completed_at`
- **Milestone**: `id`, `title`, `description`, `target_date`, `is_achieved`
- **DashboardStats**: `total_tasks`, `completed_tasks`, `pending_tasks`, `overdue_tasks`, `upcoming_deadlines`

### Frontend Components to Test

1. **TaskForm**: Form for creating/editing tasks with validation
2. **MilestoneForm**: Form for creating/editing milestones with validation
3. **DashboardStats**: Displays task statistics and upcoming deadlines
4. **StatusBadge**: Displays task status/priority/category with color coding
5. **Modal**: Reusable modal dialog with backdrop click and ESC key handling

## Functional Requirements

### 1. Bug Fix: 404 on Task/Milestone Creation

- [ ] Modify `web/lib/api.ts` to call `/tasks`, `/milestones`, `/dashboard` (no `/api` prefix)
- [ ] Verify POST `/tasks` returns 201 Created
- [ ] Verify POST `/milestones` returns 201 Created
- [ ] Verify creating a task via UI saves and displays correctly
- [ ] Verify creating a milestone via UI saves and displays correctly
- [ ] No 404 errors in browser console

### 2. Text Fix: MilestoneList Inconsistency

- [ ] Change "dias para seguir" to "dias para frente" in `web/components/MilestoneList.tsx` (line 150)

### 3. Frontend Unit Tests

- [ ] Install Vitest and React Testing Library in `web/package.json`
- [ ] Create `web/tests/TaskForm.test.tsx` — test form validation, submission, error states
- [ ] Create `web/tests/MilestoneForm.test.tsx` — test form validation, submission, error states
- [ ] Create `web/tests/DashboardStats.test.tsx` — test loading state, empty state, data display
- [ ] Create `web/tests/StatusBadge.test.tsx` — test status, priority, category variants
- [ ] Create `web/tests/Modal.test.tsx` — test open/close, ESC key, backdrop click
- [ ] Run `npm run test` successfully with ≥5 passing tests

### 4. Usability Test Plan

- [ ] Create `web/tests/TEST_PLAN.md` with structured manual test cases:
  - Dashboard: Load, stats update after create/delete
  - Tasks: Create, edit, complete, delete flows
  - Milestones: Create, edit, mark achieved, delete flows
  - Edge cases: Empty states, form validation, API offline handling
  - Responsive: Mobile, tablet, desktop viewports

### 5. Documentation

- [ ] Create `web/README.md` with setup instructions (npm install, npm run dev)
- [ ] Update root `README.md` to reflect v2.0 architecture (Backend + Frontend)
- [ ] Update `pyproject.toml` version to `2.0.0`
- [ ] Update `web/package.json` version to `2.0.0`

### 6. Regression Testing

- [ ] All 105 backend tests still pass
- [ ] Backend coverage remains at 95%+
- [ ] CI/CD pipeline green after merge

## Non-Functional Requirements

### Testing Standards

- Use **Vitest** as the test runner (fast, compatible with Vite/Next.js)
- Use **React Testing Library** for component testing (accessibility-friendly queries)
- Do not introduce E2E frameworks (Playwright/Cypress) — scope is limited to unit tests
- Minimum 5 component tests required

### Performance

- Frontend tests should complete in <30 seconds
- No performance regression in frontend bundle size

### Security

- No secrets exposed in test files
- API calls use environment variables for base URL

### Compatibility

- Support Next.js 14.x (current version)
- Support modern browsers (Chrome, Firefox, Safari, Edge)

## Out of Scope

The following are explicitly NOT included in this session:

- **E2E testing** with Cypress or Playwright
- **New features** beyond bug fixes
- **Cloud deployment** or production setup
- **Backend test coverage** increase (maintain 95%)
- **Database migration** to PostgreSQL
- **Authentication** or user management
- **Real-time updates** (WebSocket)

## Success Criteria

| # | Criterion | Verification Method |
|---|-----------|---------------------|
| 1 | POST `/tasks` returns 201 | Swagger UI + UI manual test |
| 2 | POST `/milestones` returns 201 | Swagger UI + UI manual test |
| 3 | Task creation works end-to-end | Create task via UI, verify in list |
| 4 | Milestone creation works end-to-end | Create milestone via UI, verify in list |
| 5 | `npm run test` passes with ≥5 tests | Vitest output |
| 6 | `web/tests/TEST_PLAN.md` exists | File check |
| 7 | Text "dias para frente" correct | Inspect MilestoneList.tsx |
| 8 | `web/README.md` created | File check |
| 9 | Root README reflects v2.0 | Inspect README.md |
| 10 | Version 2.0.0 in pyproject.toml | File check |
| 11 | All 105 backend tests pass | pytest output |
| 12 | CI/CD green | GitHub Actions |

## Implementation Plan

### Step 1: Fix the 404 Bug (Priority: Critical)

1. Edit `web/lib/api.ts`:
   - Change `/api/dashboard` → `/dashboard`
   - Change `/api/tasks` → `/tasks`
   - Change `/api/tasks/${id}` → `/tasks/${id}`
   - Change `/api/milestones` → `/milestones`
   - Change `/api/milestones/${id}` → `/milestones/${id}`

2. Verify fix by running backend and testing via Swagger UI or curl:
   ```bash
   curl -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Test","description":"Test","deadline":"2026-03-10","priority":"Média","category":"Geral"}'
   ```

### Step 2: Fix Text Inconsistency

1. Edit `web/components/MilestoneList.tsx` line 150:
   - Change: `${days} dias para seguir`
   - To: `${days} dias para frente`

### Step 3: Add Frontend Testing Dependencies

1. Edit `web/package.json`:
   ```json
   "devDependencies": {
     "@testing-library/jest-dom": "^6.4.0",
     "@testing-library/react": "^14.2.0",
     "@vitejs/plugin-react": "^4.2.0",
     "jsdom": "^24.0.0",
     "vitest": "^1.4.0"
   }
   ```

2. Add test script to `package.json`:
   ```json
   "scripts": {
     "test": "vitest"
   }
   ```

3. Create `web/vitest.config.ts`:
   ```typescript
   import { defineConfig } from 'vitest/config';
   import react from '@vitejs/plugin-react';
   
   export default defineConfig({
     plugins: [react()],
     test: {
       environment: 'jsdom',
       globals: true,
       setupFiles: './tests/setup.ts',
     },
   });
   ```

### Step 4: Create Component Tests

Create the following test files in `web/tests/`:

1. **TaskForm.test.tsx** — Test form rendering, validation errors, successful submission
2. **MilestoneForm.test.tsx** — Test form rendering, validation errors, successful submission
3. **DashboardStats.test.tsx** — Test loading state, null state, data rendering
4. **StatusBadge.test.tsx** — Test status variants (A Fazer, Em Progresso, Concluída, Bloqueada), priority variants
5. **Modal.test.tsx** — Test open/close, ESC key listener, backdrop click

### Step 5: Create Documentation

1. Create `web/README.md` with:
   - Prerequisites (Node.js 18+)
   - Installation steps
   - Running the development server
   - Running tests
   - Environment variables

2. Update root `README.md`:
   - Add "v2.0" badge
   - Add Frontend section (Next.js + Tailwind)
   - Update project structure diagram
   - Add "Quick Start" for full-stack setup

### Step 6: Version Bump

1. Update `pyproject.toml`:
   ```toml
   [project]
   version = "2.0.0"
   ```

2. Update `web/package.json`:
   ```json
   "version": "2.0.0"
   ```

### Step 7: Regression Testing

1. Run backend tests:
   ```bash
   poetry run pytest tests/ -v
   ```

2. Run frontend tests:
   ```bash
   cd web && npm run test
   ```

3. Verify both pass before opening PR

## Risks & Side Effects

| Risk | Impact | Mitigation |
|------|--------|------------|
| Fixing frontend API paths may break if backend routes change | Medium | Document the dependency; consider adding API prefix to backend instead |
| Vitest configuration may conflict with Next.js | Low | Use standard jsdom environment; avoid complex mocks |
| Text change may affect i18n consistency | Low | This is a single correction; no broader i18n system in place |
| Version bump may affect dependency resolution | Low | Test thoroughly with `poetry lock` and `npm install` |

## Open Questions

1. **Should the `/api` prefix be added to the backend instead of removed from the frontend?**
   
   Adding `/api` to all backend routes is arguably more "RESTful" and would match what the frontend expects. However, this requires modifying three router files and could introduce regressions. The proposed fix (removing `/api` from frontend) is safer and achieves the same user-facing result.

2. **Should a minimum test coverage threshold be enforced in Vitest config?**
   
   The BRIEF suggests establishing a minimum threshold (e.g., 70%). For this initial test suite, we recommend starting without a强制 threshold to allow flexibility, but adding one after the first few releases is advisable.

3. **Should the frontend use TypeScript strict mode for tests?**
   
   The project already uses TypeScript. Tests should follow the same type-checking rules as production code.

4. **How to handle environment-specific API URLs?**
   
   Currently, `web/lib/api.ts` uses `process.env.NEXT_PUBLIC_API_URL`. Ensure `.env.local` is properly documented in `web/README.md`.
