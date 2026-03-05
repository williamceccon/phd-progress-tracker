# SPEC.md — Web Tests, Bug Fixes & Version 2.0 Polish

## Overview

This specification document provides detailed technical implementation guidance for the v2.0 polish phase of the PhD Progress Tracker web platform. The work includes fixing critical bugs, adding frontend unit tests, fixing minor UI issues, and releasing version 2.0.

## Affected Files

### Direct Changes

| Layer | File | Change Type | Description |
|-------|------|-------------|-------------|
| Frontend | `web/lib/api.ts` | Modify | Remove `/api` prefix from all endpoints |
| Frontend | `web/components/MilestoneList.tsx` | Modify | Fix text "dias para seguir" → "dias para frente" (line 150) |
| Config | `pyproject.toml` | Modify | Update version to `2.0.0` |
| Config | `web/package.json` | Modify | Add test dependencies + update version to `2.0.0` |
| Config | `web/vitest.config.ts` | Create | Vitest configuration for frontend testing |
| Tests | `web/tests/setup.ts` | Create | Test setup with React Testing Library |
| Tests | `web/tests/TaskForm.test.tsx` | Create | Unit tests for TaskForm component |
| Tests | `web/tests/MilestoneForm.test.tsx` | Create | Unit tests for MilestoneForm component |
| Tests | `web/tests/DashboardStats.test.tsx` | Create | Unit tests for DashboardStats component |
| Tests | `web/tests/StatusBadge.test.tsx` | Create | Unit tests for StatusBadge component |
| Tests | `web/tests/Modal.test.tsx` | Create | Unit tests for Modal component |
| Tests | `web/tests/TEST_PLAN.md` | Create | Manual usability test plan |
| Docs | `web/README.md` | Create | Frontend setup instructions |
| Docs | `README.md` | Modify | Update for v2.0 architecture |

### Indirect Dependencies

| Layer | File | Reason |
|-------|------|--------|
| Backend | `phd_progress_tracker/api/routes/tasks.py` | Verified: uses `/tasks` prefix (no change needed) |
| Backend | `phd_progress_tracker/api/routes/milestones.py` | Verified: uses `/milestones` prefix (no change needed) |
| Backend | `phd_progress_tracker/api/routes/dashboard.py` | Verified: uses `/dashboard` prefix (no change needed) |
| Frontend | `web/lib/types.ts` | Type definitions used by tests |
| Frontend | `web/lib/utils.ts` | Utility functions used by components |

## Implementation Plan (Ordered Steps)

### Step 1: Fix the 404 Bug (Priority: Critical)

**Objective**: Resolve the route mismatch causing 404 errors when creating tasks and milestones.

**Root Cause Analysis**:
- Backend routers define prefixes: `/tasks`, `/milestones`, `/dashboard` (see `phd_progress_tracker/api/routes/tasks.py:15`, `milestones.py:18`)
- Frontend API client calls: `/api/tasks`, `/api/milestones`, `/api/dashboard` (see `web/lib/api.ts:53,61,72`)
- The `/api` prefix mismatch causes FastAPI to return 404 Not Found

**Implementation**:
```typescript
// File: web/lib/api.ts
// Before (lines 53, 61, 66, 72, 81, 90, 100, 105, 111, 120, 129):
'/api/dashboard' → '/dashboard'
'/api/tasks' → '/tasks'
'/api/tasks/${id}' → '/tasks/${id}'
'/api/milestones' → '/milestones'
'/api/milestones/${id}' → '/milestones/${id}'
```

**Verification**:
```bash
# Test via curl after backend is running
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test task","deadline":"2026-03-10","priority":"Média","category":"Geral"}'
# Should return 201 Created

curl -X POST http://localhost:8000/milestones \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Milestone","description":"Test milestone","target_date":"2026-06-01"}'
# Should return 201 Created
```

### Step 2: Fix Text Inconsistency

**Objective**: Correct the grammatical error in MilestoneList component.

**Implementation**:
```typescript
// File: web/components/MilestoneList.tsx, line 150
// Before:
`${days} dias para seguir`
// After:
`${days} dias para frente`
```

### Step 3: Add Frontend Testing Dependencies

**Objective**: Install Vitest and React Testing Library for component unit tests.

**Implementation**:
```json
// File: web/package.json - Add to devDependencies
{
  "@testing-library/jest-dom": "^6.4.0",
  "@testing-library/react": "^14.2.0",
  "@vitejs/plugin-react": "^4.2.0",
  "jsdom": "^24.0.0",
  "vitest": "^1.4.0"
}

// Add test script
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run"
  }
}
```

**Vitest Configuration**:
```typescript
// File: web/vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.ts',
    include: ['tests/**/*.test.{ts,tsx}'],
  },
});
```

**Test Setup**:
```typescript
// File: web/tests/setup.ts
import '@testing-library/jest-dom';
```

### Step 4: Create Component Unit Tests

**Objective**: Add at least 5 unit tests covering core components.

#### 4.1 TaskForm Tests

**File**: `web/tests/TaskForm.test.tsx`

| Test Case | Description | Expected Behavior |
|-----------|-------------|-------------------|
| Renders form fields | Check all input fields render | Title, description, deadline, category, priority inputs visible |
| Shows validation errors | Submit empty form | Error messages displayed for required fields |
| Calls onSubmit with valid data | Fill and submit valid form | onSubmit called with correct TaskCreate object |
| Resets form on close | Open form, add data, close, reopen | Form shows default values |
| Shows loading state | Submit with isSubmitting=true | Submit button shows loading indicator |

#### 4.2 MilestoneForm Tests

**File**: `web/tests/MilestoneForm.test.tsx`

| Test Case | Description | Expected Behavior |
|-----------|-------------|-------------------|
| Renders form fields | Check all input fields render | Title, description, target_date inputs visible |
| Shows validation errors | Submit empty form | Error messages for title, description, target_date |
| Calls onSubmit with valid data | Fill and submit valid form | onSubmit called with correct MilestoneCreate object |
| Populates edit mode | Pass existing milestone | Form pre-filled with milestone data |

#### 4.3 DashboardStats Tests

**File**: `web/tests/DashboardStats.test.tsx`

| Test Case | Description | Expected Behavior |
|-----------|-------------|-------------------|
| Shows loading skeleton | isLoading=true | Skeleton placeholders displayed |
| Returns null when no stats | stats=null | Component returns null (no render) |
| Displays stats correctly | Pass valid stats object | All stat cards show correct values |
| Shows percentage for completed | stats with total>0 | Completed card shows percentage |
| Renders upcoming deadlines | stats with upcoming_deadlines | Deadline list displayed |

#### 4.4 StatusBadge Tests

**File**: `web/tests/StatusBadge.test.tsx`

| Test Case | Description | Expected Behavior |
|-----------|-------------|-------------------|
| Status: A Fazer | variant="status", value="A Fazer" | Gray background and text |
| Status: Em Progresso | variant="status", value="Em Progresso" | Amber background and text |
| Status: Concluída | variant="status", value="Concluída" | Green background and text |
| Status: Bloqueada | variant="status", value="Bloqueada" | Red background and text |
| Priority: Baixa | variant="priority", value="Baixa" | Light gray badge |
| Priority: Crítica | variant="priority", value="Crítica" | Red badge |
| Category variant | variant="category", value="RSL" | Purple badge |

#### 4.5 Modal Tests

**File**: `web/tests/Modal.test.tsx`

| Test Case | Description | Expected Behavior |
|-----------|-------------|-------------------|
| Does not render when closed | isOpen=false | Modal not in DOM |
| Renders when open | isOpen=true | Modal visible with title |
| Closes on ESC key | Press Escape key | onClose called |
| Closes on backdrop click | Click outside modal | onClose called |
| Does not close on content click | Click inside modal | onClose not called |
| Renders children | Pass child content | Children visible inside modal |

### Step 5: Create Documentation

**Objective**: Document the frontend setup and update root README for v2.0.

#### 5.1 Frontend README

**File**: `web/README.md`

```markdown
# PhD Progress Tracker - Web Frontend

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend running on http://localhost:8000

## Installation

```bash
cd web
npm install
```

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

```bash
npm run dev
# Open http://localhost:3000
```

## Testing

```bash
npm run test      # Watch mode
npm run test:run  # Single run
```

## Build

```bash
npm run build
npm start
```

## Tech Stack

- Next.js 14.x
- React 18.x
- Tailwind CSS 3.4
- Vitest + React Testing Library
```

#### 5.2 Root README Update

**File**: `README.md`

- Add v2.0 badge
- Add Frontend section with Next.js + Tailwind
- Update project structure diagram
- Add "Quick Start" for full-stack setup (Backend + Frontend)
- Keep CLI documentation for backward compatibility

### Step 6: Version Bump

**Objective**: Update version numbers to 2.0.0.

**Implementation**:
```toml
# File: pyproject.toml
[project]
version = "2.0.0"
```

```json
// File: web/package.json
{
  "version": "2.0.0"
}
```

### Step 7: Regression Testing

**Objective**: Ensure all existing tests still pass.

**Commands**:
```bash
# Backend tests
poetry run pytest tests/ -v

# Frontend tests
cd web && npm run test:run

# Lint (if configured)
cd web && npm run lint
```

## API / Schema Design

### Backend Route Verification

| Endpoint | Method | Status Code | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/tasks` | GET | 200 | - | `Task[]` |
| `/tasks` | POST | 201 | `TaskCreate` | `Task` |
| `/tasks/{id}` | GET | 200 | - | `Task` |
| `/tasks/{id}` | PATCH | 200 | `TaskUpdate` | `Task` |
| `/tasks/{id}` | DELETE | 204 | - | - |
| `/milestones` | GET | 200 | - | `Milestone[]` |
| `/milestones` | POST | 201 | `MilestoneCreate` | `Milestone` |
| `/milestones/{id}` | GET | 200 | - | `Milestone` |
| `/milestones/{id}` | PATCH | 200 | `MilestoneUpdate` | `Milestone` |
| `/milestones/{id}` | DELETE | 204 | - | - |
| `/dashboard` | GET | 200 | - | `DashboardStats` |

### Frontend Type Definitions

```typescript
// File: web/lib/types.ts (existing - verified)
interface Task {
  id: string;
  title: string;
  description: string;
  deadline: string;
  status: TaskStatus;
  priority: TaskPriority;
  category: string;
  created_at: string;
  completed_at?: string;
}

interface TaskCreate {
  title: string;
  description: string;
  deadline: string;
  priority: TaskPriority;
  category: string;
}

interface Milestone {
  id: string;
  title: string;
  description: string;
  target_date: string;
  is_achieved: boolean;
}

interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  overdue_tasks: number;
  upcoming_deadlines: Task[];
}
```

## Risks & Side Effects

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-------------|
| Route fix breaks other integrations | Medium | Low | Test all API endpoints; verify Swagger UI |
| Vitest config conflicts with Next.js | Low | Low | Use jsdom environment; avoid complex mocks |
| Text change affects i18n consistency | Low | Low | Single correction; no i18n system in use |
| Version bump affects dependencies | Low | Low | Run `poetry lock` and `npm install` after change |
| Frontend tests fail on CI | Medium | Medium | Ensure jsdom environment; mock window/document |

## Open Questions

1. **Should the `/api` prefix be added to backend instead of removed from frontend?**
   
   **Recommendation**: Remove from frontend (current approach). Adding `/api` to backend requires modifying three router files and could introduce regressions. The frontend change is safer and achieves the same result.

2. **Should a minimum test coverage threshold be enforced?**
   
   **Recommendation**: Start without enforcement for flexibility. Consider adding 70% threshold after v2.0 release once test suite matures.

3. **How to handle API offline scenarios in tests?**
   
   **Recommendation**: Use MSW (Mock Service Worker) for network mocking. For v2.0, simple jest.fn() mocks are sufficient.

4. **Should TypeScript strict mode be enforced in tests?**
   
   **Recommendation**: Yes, maintain consistency with production code. Tests should follow same type-checking rules.

## Success Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | POST `/tasks` returns 201 | `curl -X POST http://localhost:8000/tasks ...` |
| 2 | POST `/milestones` returns 201 | `curl -X POST http://localhost:8000/milestones ...` |
| 3 | Task creation works end-to-end | Create task via UI at http://localhost:3000/tasks |
| 4 | Milestone creation works end-to-end | Create milestone via UI at http://localhost:3000/milestones |
| 5 | `npm run test:run` passes | ≥5 tests passing |
| 6 | `web/tests/TEST_PLAN.md` exists | File check |
| 7 | Text "dias para frente" correct | Inspect MilestoneList.tsx line 150 |
| 8 | `web/README.md` created | File check |
| 9 | Root README reflects v2.0 | Check for "v2.0" badge and frontend section |
| 10 | Version 2.0.0 in pyproject.toml | `grep "version = \"2.0.0\"" pyproject.toml` |
| 11 | All 105 backend tests pass | `poetry run pytest tests/ -v` |
| 12 | CI/CD green | GitHub Actions workflow passes |

## Out of Scope

The following are explicitly NOT included in this specification:

- **E2E testing** with Cypress or Playwright
- **New features** beyond bug fixes
- **Cloud deployment** or production setup
- **Backend test coverage** increase (maintain 95%)
- **Database migration** to PostgreSQL
- **Authentication** or user management
- **Real-time updates** via WebSocket
