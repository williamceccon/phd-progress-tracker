# Technical Specification: Local Web Frontend

## Overview

This document provides comprehensive technical specifications for implementing the Local Web Frontend feature (Phase 3 of the PhD Progress Tracker migration). The frontend will be a Next.js application with TypeScript and Tailwind CSS that consumes the existing FastAPI backend, providing a visual dashboard for managing PhD tasks and milestones.

## Implementation Context

The backend API has been analyzed and the following details inform this specification:

- **Backend URL**: `http://localhost:8000`
- **API Prefix**: `/api` (FastAPI default)
- **Date Format**: ISO 8601 (`YYYY-MM-DD`) for dates, ISO datetime for timestamps
- **Language**: Backend uses Portuguese enum values for status and priority fields

## 1. Project Architecture

### 1.1 Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | Next.js | 14.x (App Router) |
| Language | TypeScript | 5.x |
| Styling | Tailwind CSS | 3.x |
| HTTP Client | Native fetch API | - |
| State Management | React useState/useEffect | React 18.x |
| Build Tool | Next.js built-in | - |

### 1.2 Frontend Directory Structure

```
web/
├── package.json
├── next.config.js
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Dashboard (/)
│   ├── globals.css
│   └── tasks/
│       └── page.tsx          # Tasks (/tasks)
│   └── milestones/
│       └── page.tsx          # Milestones (/milestones)
├── components/
│   ├── Header.tsx
│   ├── DashboardStats.tsx
│   ├── TaskList.tsx
│   ├── TaskForm.tsx
│   ├── MilestoneList.tsx
│   ├── MilestoneForm.tsx
│   ├── Modal.tsx
│   ├── Button.tsx
│   ├── Card.tsx
│   └── StatusBadge.tsx
└── lib/
    ├── api.ts
    ├── types.ts
    └── utils.ts
```

## 2. API Integration Specification

### 2.1 Backend Modification Required

**File: `phd_progress_tracker/api/main.py`**

Add CORS middleware to allow frontend requests:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2.2 REST API Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/dashboard` | Fetch dashboard statistics | - | `DashboardStats` |
| GET | `/api/tasks` | List all tasks | - | `Task[]` |
| POST | `/api/tasks` | Create new task | `TaskCreate` | `Task` |
| GET | `/api/tasks/{id}` | Get single task | - | `Task` |
| PATCH | `/api/tasks/{id}` | Update task | `TaskUpdate` | `Task` |
| DELETE | `/api/tasks/{id}` | Delete task | - | `204 No Content` |
| GET | `/api/milestones` | List all milestones | - | `Milestone[]` |
| POST | `/api/milestones` | Create milestone | `MilestoneCreate` | `Milestone` |
| GET | `/api/milestones/{id}` | Get single milestone | - | `Milestone` |
| PATCH | `/api/milestones/{id}` | Update milestone | `MilestoneUpdate` | `Milestone` |
| DELETE | `/api/milestones/{id}` | Delete milestone | - | `204 No Content` |

### 2.3 TypeScript Type Definitions

**File: `web/lib/types.ts`**

```typescript
// Enums matching backend Portuguese values
export type TaskStatus = 'A Fazer' | 'Em Progresso' | 'Concluída' | 'Bloqueada';
export type TaskPriority = 'Baixa' | 'Média' | 'Alta' | 'Crítica';

export interface Task {
  id: string;
  title: string;
  description: string;
  deadline: string;        // ISO date: "2024-12-31"
  status: TaskStatus;
  priority: TaskPriority;
  category: string;
  created_at: string;     // ISO datetime: "2024-01-15T10:30:00"
  completed_at: string | null;
}

export interface TaskCreate {
  title: string;
  description: string;
  deadline: string;
  category?: string;
  priority?: TaskPriority;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  deadline?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  category?: string;
}

export interface Milestone {
  id: string;
  title: string;
  description: string;
  target_date: string;    // ISO date: "2024-12-31"
  is_achieved: boolean;
}

export interface MilestoneCreate {
  title: string;
  description: string;
  target_date: string;
}

export interface MilestoneUpdate {
  title?: string;
  description?: string;
  target_date?: string;
  is_achieved?: boolean;
}

export interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  overdue_tasks: number;
  upcoming_deadlines: Task[];
}

export interface ApiError {
  detail: string;
}
```

### 2.4 API Client Implementation

**File: `web/lib/api.ts`**

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// Dashboard API
export const dashboardApi = {
  getStats: () => fetchApi<DashboardStats>('/api/dashboard'),
};

// Tasks API
export const tasksApi = {
  list: () => fetchApi<Task[]>('/api/tasks'),
  get: (id: string) => fetchApi<Task>(`/api/tasks/${id}`),
  create: (task: TaskCreate) => 
    fetchApi<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    }),
  update: (id: string, task: TaskUpdate) => 
    fetchApi<Task>(`/api/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(task),
    }),
  delete: (id: string) => 
    fetchApi<void>(`/api/tasks/${id}`, {
      method: 'DELETE',
    }),
};

// Milestones API
export const milestonesApi = {
  list: () => fetchApi<Milestone[]>('/api/milestones'),
  get: (id: string) => fetchApi<Milestone>(`/api/milestones/${id}`),
  create: (milestone: MilestoneCreate) => 
    fetchApi<Milestone>('/api/milestones', {
      method: 'POST',
      body: JSON.stringify(milestone),
    }),
  update: (id: string, milestone: MilestoneUpdate) => 
    fetchApi<Milestone>(`/api/milestones/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(milestone),
    }),
  delete: (id: string) => 
    fetchApi<void>(`/api/milestones/${id}`, {
      method: 'DELETE',
    }),
};
```

## 3. UI/UX Specification

### 3.1 Design System

#### Color Palette

| Name | Hex Code | Usage |
|------|----------|-------|
| Primary | `#3B82F6` | Buttons, links, active states |
| Primary Dark | `#2563EB` | Button hover states |
| Secondary | `#64748B` | Secondary text, borders |
| Success | `#10B981` | Completed tasks, success messages |
| Warning | `#F59E0B` | In-progress, pending items |
| Danger | `#EF4444` | Delete buttons, overdue items |
| Background | `#F8FAFC` | Page background |
| Card Background | `#FFFFFF` | Card and modal backgrounds |
| Text Primary | `#1E293B` | Main text |
| Text Secondary | `#64748B` | Secondary text |
| Border | `#E2E8F0` | Borders and dividers |

#### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Heading 1 | Inter | 32px | 700 |
| Heading 2 | Inter | 24px | 600 |
| Heading 3 | Inter | 18px | 600 |
| Body | Inter | 16px | 400 |
| Small | Inter | 14px | 400 |
| Caption | Inter | 12px | 400 |

#### Spacing System

- Base unit: 4px
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64px
- Container max-width: 1200px
- Card padding: 24px
- Section gap: 32px

#### Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 640px | Single column, stacked cards |
| Tablet | 640px - 1024px | Two columns where appropriate |
| Desktop | > 1024px | Full layout with sidebar |

### 3.2 Component Specifications

#### Header Component

- Fixed position at top
- Height: 64px
- Background: White with bottom border
- Logo/Title on left: "PhD Progress Tracker"
- Navigation links on right: Dashboard, Tasks, Milestones
- Active link indicator: Primary color underline
- Mobile: Hamburger menu with slide-out navigation

#### Dashboard Page (`/`)

**Hero Section**
- Welcome message: "Welcome to your PhD Progress Tracker"
- Subtitle showing current date

**Statistics Cards (4 cards in grid)**
- Total Tasks: Blue card with count
- Completed: Green card with count and percentage
- Pending: Amber card with count
- Overdue: Red card with count (only show if > 0)

**Upcoming Deadlines Section**
- Title: "Upcoming Deadlines (Next 7 Days)"
- List of tasks sorted by deadline
- Each item shows: Title, Deadline (relative: "in 3 days"), Priority badge
- Empty state: "No upcoming deadlines"

#### Tasks Page (`/tasks`)

**Header**
- Title: "Tasks"
- "Add Task" button (primary style)

**Task List/Table**
- Columns: Title, Category, Deadline, Status, Priority, Actions
- Sortable by deadline and status
- Row hover effect

**Task Row**
- Title with truncate (max 30 chars)
- Category badge
- Deadline with relative date ("in 2 days", "3 days ago")
- Status badge with color coding:
  - "A Fazer": Gray
  - "Em Progresso": Amber
  - "Concluída": Green
  - "Bloqueada": Red
- Priority badge:
  - "Baixa": Gray
  - "Média": Blue
  - "Alta": Orange
  - "Crítica": Red
- Action buttons: Edit (icon), Delete (icon)

**Task Form (Modal)**
- Fields:
  - Title (required, text input)
  - Description (required, textarea)
  - Deadline (required, date input)
  - Category (select with options: Geral, Coleta de Dados, Análise, Escrita, Revisão)
  - Priority (select with options: Baixa, Média, Alta, Crítica)
  - Status (select, only in edit mode)
- Buttons: Cancel (secondary), Save (primary)
- Validation: Inline error messages

#### Milestones Page (`/milestones`)

**Header**
- Title: "Milestones"
- "Add Milestone" button (primary style)

**Milestone List**
- Card layout with grid (2 columns on desktop, 1 on mobile)
- Each card shows:
  - Title (large)
  - Description
  - Target Date with countdown ("12 days to go" or "Achieved!")
  - Status toggle: Checkbox to mark as achieved
  - Actions: Edit, Delete

**Milestone Form (Modal)**
- Fields:
  - Title (required)
  - Description (required)
  - Target Date (required, date input)
- Buttons: Cancel, Save

### 3.3 Component States

#### Loading States
- Skeleton loaders for cards and lists
- Spinner for button loading (disabled state with spinner)

#### Error States
- Toast notifications for API errors
- Inline error messages for form validation
- Empty states with helpful messages and action buttons

#### Empty States
- Dashboard: "No tasks yet. Create your first task!"
- Tasks: "No tasks found. Click 'Add Task' to get started."
- Milestones: "No milestones set. Plan your first4. Implementation Plan milestone!"

## 

### Phase 1: Project Setup

1. Initialize Next.js project in `web/` directory
2. Configure Tailwind with custom colors
3. Set up project structure

### Phase 2: API Integration

4. Add CORS to backend
5. Create API client

### Phase 3: Dashboard

6. Create dashboard types and API function
7. Implement DashboardStats component
8. Build Phase 4: dashboard page

### Tasks

9. Implement TaskList component
10. Implement TaskForm component
11. Add CRUD operations

### Phase 5: Milestones

12. Implement MilestoneList component
13. Implement MilestoneForm component
14. Add CRUD operations

### Phase 6: Polish

15. Responsive navigation
16. Loading skeletons
17. Toast notifications

## 5. Environment Configuration

**Frontend (`web/.env.local`)**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running the Application

**Terminal 1 - Backend:**
```bash
poetry run uvicorn phd_progress_tracker.api.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd web
npm run dev
```

Access at: `http://localhost:3000`

## 6. Technical Decisions

### 6.1 State Management
- Use React `useState` and `useEffect` hooks

### 6.2 Form Handling
- Controlled components with local state

### 6.3 Date Handling
- Native JavaScript Date with helper utilities
- Use ISO strings for API, display with `toLocaleDateString()`

### 6.4 Modal Implementation
- Custom Modal component

### 6.5 Error Handling
- Try-catch with toast notifications

## 7. Success Criteria

1. Frontend initializes with `npm run dev` on port 3000
2. Dashboard displays statistics from `/api/dashboard`
3. Tasks CRUD works via UI
4. Milestones CRUD works via UI
5. All existing backend tests pass
6. Responsive design works on mobile and desktop
7. No console errors in browser

## 8. File Manifest

### New Files to Create

| File Path | Description |
|-----------|-------------|
| `web/package.json` | Next.js project configuration |
| `web/next.config.js` | Next.js configuration |
| `web/tsconfig.json` | TypeScript configuration |
| `web/tailwind.config.ts` | Tailwind CSS configuration |
| `web/postcss.config.js` | PostCSS configuration |
| `web/.env.local` | Environment variables |
| `web/app/layout.tsx` | Root layout with Header |
| `web/app/page.tsx` | Dashboard page |
| `web/app/globals.css` | Global styles |
| `web/app/tasks/page.tsx` | Tasks management page |
| `web/app/milestones/page.tsx` | Milestones management page |
| `web/components/Header.tsx` | Navigation header |
| `web/components/DashboardStats.tsx` | Statistics display |
| `web/components/TaskList.tsx` | Task list/table |
| `web/components/TaskForm.tsx` | Task create/edit form |
| `web/components/MilestoneList.tsx` | Milestone list |
| `web/components/MilestoneForm.tsx` | Milestone create/edit form |
| `web/components/Modal.tsx` | Reusable modal component |
| `web/components/Button.tsx` | Styled button component |
| `web/components/Card.tsx` | Card container component |
| `web/components/StatusBadge.tsx` | Status/priority badge |
| `web/lib/api.ts` | API client functions |
| `web/lib/types.ts` | TypeScript type definitions |
| `web/lib/utils.ts` | Utility functions |

### Files to Modify

| File | Change |
|------|--------|
| `phd_progress_tracker/api/main.py` | Add CORS middleware |

---

*Specification created for implementation planning. Subject to revision based on implementation feedback.*
