# PRD — Local Web Frontend

## Overview

Create a modern, user-friendly web frontend to consume the existing FastAPI backend, providing a visual dashboard for managing PhD tasks and milestones. This is Phase 3 of the migration from a pure CLI tool to a SaaS platform. The frontend will allow users to interact with their tasks and milestones through a web interface without modifying the existing Python backend or CLI.

## Affected Files

### New Files (Frontend)

| File | Description |
|------|-------------|
| `web/package.json` | Next.js project configuration |
| `web/next.config.js` | Next.js configuration |
| `web/tsconfig.json` | TypeScript configuration |
| `web/tailwind.config.ts` | Tailwind CSS configuration |
| `web/postcss.config.js` | PostCSS configuration |
| `web/app/layout.tsx` | Root layout component |
| `web/app/page.tsx` | Home page (Dashboard) |
| `web/app/tasks/page.tsx` | Tasks management page |
| `web/app/milestones/page.tsx` | Milestones management page |
| `web/app/globals.css` | Global styles |
| `web/components/Header.tsx` | Navigation header component |
| `web/components/DashboardStats.tsx` | Statistics display component |
| `web/components/TaskList.tsx` | Task list component |
| `web/components/TaskForm.tsx` | Task create/edit form |
| `web/components/MilestoneList.tsx` | Milestone list component |
| `web/components/MilestoneForm.tsx` | Milestone create/edit form |
| `web/lib/api.ts` | API client utility |
| `web/lib/types.ts` | TypeScript type definitions |

### Files to Modify (Backend)

| File | Change Type | Description |
|------|-------------|-------------|
| `phd_progress_tracker/api/main.py` | Modify | Add CORS middleware configuration |
| `pyproject.toml` | No change | Frontend has separate package.json |

### Files Unchanged

| File | Reason |
|------|--------|
| `phd_progress_tracker/cli/commands.py` | CLI remains unchanged |
| `phd_progress_tracker/models/task.py` | Domain models unchanged |
| `phd_progress_tracker/models/milestone.py` | Domain models unchanged |
| `phd_progress_tracker/utils/database.py` | Database layer unchanged |
| `phd_progress_tracker/api/routes/*.py` | API routes unchanged |

## Implementation Plan

### Phase 1: Project Setup

1. **Initialize Next.js project** in `web/` directory with TypeScript and App Router
2. **Configure Tailwind CSS** for styling
3. **Set up project structure** with app directory and components folder

### Phase 2: API Integration

4. **Add CORS middleware** to FastAPI backend to allow requests from frontend localhost port
5. **Create TypeScript types** matching API schemas (Task, Milestone, DashboardResponse)
6. **Implement API client** in `lib/api.ts` with fetch functions for all endpoints

### Phase 3: Dashboard View

7. **Create Dashboard page** displaying:
   - Summary statistics (total, completed, pending, overdue tasks)
   - List of upcoming deadlines (next 7 days)
8. **Implement DashboardStats component** for displaying statistics
9. **Connect to `/api/dashboard` endpoint**

### Phase 4: Tasks View

10. **Create Tasks page** with full CRUD functionality
11. **Implement TaskList component** displaying all tasks in a list/grid format
12. **Implement TaskForm component** for creating and editing tasks
13. **Add task actions**: create, read, update (PATCH), delete
14. **Connect to `/api/tasks` endpoints**

### Phase 5: Milestones View

15. **Create Milestones page** with full CRUD functionality
16. **Implement MilestoneList component** displaying all milestones
17. **Implement MilestoneForm component** for creating and editing milestones
18. **Add milestone actions**: create, read, update (PATCH), delete
19. **Connect to `/api/milestones` endpoints**

### Phase 6: Navigation and Polish

20. **Implement Header component** with navigation links
21. **Add responsive styling** for mobile and desktop
22. **Add loading and error states** for better UX
23. **Test full integration** with backend API

## API / Schema Design

### Frontend to Backend Communication

The frontend will communicate with the existing FastAPI backend running on `http://localhost:8000`.

#### REST Endpoints Consumed

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Fetch dashboard statistics |
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create new task |
| GET | `/api/tasks/{task_id}` | Get single task |
| PATCH | `/api/tasks/{task_id}` | Update task |
| DELETE | `/api/tasks/{task_id}` | Delete task |
| GET | `/api/milestones` | List all milestones |
| POST | `/api/milestones` | Create new milestone |
| GET | `/api/milestones/{milestone_id}` | Get single milestone |
| PATCH | `/api/milestones/{milestone_id}` | Update milestone |
| DELETE | `/api/milestones/{milestone_id}` | Delete milestone |

#### TypeScript Types

```typescript
// Task types
type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';
type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

interface Task {
  id: string;
  title: string;
  description: string;
  deadline: string; // ISO date format
  status: TaskStatus;
  priority: TaskPriority;
  category: string;
  created_at: string; // ISO datetime
  completed_at: string | null;
}

interface TaskCreate {
  title: string;
  description: string;
  deadline: string;
  category?: string;
  priority?: TaskPriority;
}

interface TaskUpdate {
  title?: string;
  description?: string;
  deadline?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  category?: string;
}

// Milestone types
interface Milestone {
  id: string;
  title: string;
  description: string;
  target_date: string; // ISO date format
  is_achieved: boolean;
}

interface MilestoneCreate {
  title: string;
  description: string;
  target_date: string;
}

interface MilestoneUpdate {
  title?: string;
  description?: string;
  target_date?: string;
  is_achieved?: boolean;
}

// Dashboard types
interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  overdue_tasks: number;
  upcoming_deadlines: Task[];
}
```

#### CORS Configuration

The FastAPI backend requires CORS middleware to allow the frontend to communicate:

```python
# Required addition to phd_progress_tracker/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## UI/UX Design

### Layout Structure

- **Header**: Fixed top navigation with logo and nav links (Dashboard, Tasks, Milestones)
- **Main Content**: Centered container with page-specific content
- **Responsive**: Mobile-first design with breakpoints for tablet and desktop

### Page Designs

#### Dashboard Page (`/`)

- Hero section with welcome message
- Statistics cards showing:
  - Total tasks
  - Completed tasks
  - Pending tasks
  - Overdue tasks
- Upcoming deadlines list (next 7 days)

#### Tasks Page (`/tasks`)

- "Add Task" button opening a modal or inline form
- Task list/grid with columns: Title, Category, Deadline, Status, Priority
- Each task row has Edit and Delete actions
- Status can be toggled (mark complete/incomplete)

#### Milestones Page (`/milestones`)

- "Add Milestone" button
- Milestone list showing Title, Target Date, Status
- Toggle achievement status
- Edit and Delete actions

### Styling

- **Color Palette**: Use professional, academic-themed colors
  - Primary: Blue (#3B82F6)
  - Secondary: Slate (#64748B)
  - Success: Green (#10B981)
  - Warning: Amber (#F59E0B)
  - Danger: Red (#EF4444)
- **Components**: Clean, modern UI with cards, buttons, and forms
- **Tailwind CSS**: Utility-first styling for rapid development

## Out of Scope

The following features are explicitly excluded from this phase:

- User authentication or login screens
- Multi-user support
- Cloud deployment or hosting setup
- Complex drag-and-drop Kanban boards
- Advanced charts or graphs
- Real-time WebSocket updates
- File upload/download functionality
- Email notifications

## Success Criteria

1. **Frontend Project**: Successfully initializes and runs locally with `npm run dev`
2. **Dashboard Display**: UI successfully fetches and displays data from `/api/dashboard`
3. **Task CRUD**: User can create, read, update, and delete tasks via the UI
4. **Milestone CRUD**: User can create, read, update, and delete milestones via the UI
5. **No Breaking Changes**: All existing backend tests still pass
6. **Coverage Maintained**: Python backend maintains 95%+ test coverage
7. **Responsive Design**: UI works on both mobile and desktop viewports

## Risks & Side Effects

### Technical Risks

1. **CORS Configuration**: The backend must be updated with CORS middleware. This is a minor change but required for frontend-backend communication.
2. **API State Management**: Frontend must handle loading, error, and success states properly when communicating with the API.
3. **Date Handling**: JavaScript date handling must correctly parse ISO date strings from the API.
4. **Concurrent Access**: SQLite may have concurrency issues if both CLI and web frontend are used simultaneously (mitigated by single-user local use).

### Potential Side Effects

1. **Database File**: Both CLI and web frontend will read/write to the same SQLite database file (`data/phd_tracker.db`), ensuring data consistency across interfaces.
2. **No Migration Needed**: The frontend uses existing API endpoints, so no database migration is required.
3. **Parallel Development**: Both CLI and web frontend can be used simultaneously during development.

## Open Questions

1. **Q**: Should the frontend automatically start the backend server, or should users run them separately?
   - **A**: Run separately for clarity. User starts backend with `poetry run uvicorn` and frontend with `npm run dev`.

2. **Q**: Should we use a state management library (Redux, Zustand) or React Context?
   - **A**: Use React Context or local state for simplicity. This is a small-scale MVP, complex state management is not needed.

3. **Q**: Should we add a "refresh" button to manually reload data, or use automatic polling?
   - **A**: Add a manual refresh button for simplicity. Auto-refresh can be considered in a future phase.

4. **Q**: How should we handle form validation errors from the API?
   - **A**: Display validation error messages inline in the form, matching the API response structure.

5. **Q**: Should the frontend be in a `web/` or `frontend/` directory?
   - **A**: Use `web/` as it aligns with the web application nature of the project.

## Dependencies

### Frontend (Node.js)

- Next.js 14+ (App Router)
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- No additional UI libraries required (use native HTML/CSS)

### Backend (Python)

- No new Python dependencies required
- FastAPI CORS middleware (built-in)

## Testing Strategy

### Frontend Testing (Future Phase)

- Component testing with React Testing Library
- Integration testing with API mock
- Manual browser testing for UX validation

### Backend Testing

- All existing tests must continue to pass
- Verify CORS configuration does not break existing API functionality
- Run: `poetry run pytest --cov=phd_progress_tracker`

## Documentation

After implementation, create:

1. **README.md** in `web/` directory with setup instructions
2. Update main **README.md** with frontend setup and usage
3. Add to **AGENTS.md** any new commands or conventions
