# Test Report — web-tests-v2-polish

Date: 2026-03-05

## Test Plan

### Test Cases to Implement

| Test Case | File | Purpose | Expected Behavior |
|-----------|------|---------|-------------------|
| Renders form fields | `web/tests/TaskForm.test.tsx` | Check all input fields render | Title, description, deadline, category, priority inputs visible |
| Shows validation errors | `web/tests/TaskForm.test.tsx` | Submit empty form | Error messages displayed for required fields |
| Calls onSubmit with valid data | `web/tests/TaskForm.test.tsx` | Fill and submit valid form | onSubmit called with correct TaskCreate object |
| Resets form on close | `web/tests/TaskForm.test.tsx` | Open form, add data, close, reopen | Form shows default values |
| Shows loading state | `web/tests/TaskForm.test.tsx` | Submit with isSubmitting=true | Submit button shows loading indicator |
| Renders form fields | `web/tests/MilestoneForm.test.tsx` | Check all input fields render | Title, description, target_date inputs visible |
| Shows validation errors | `web/tests/MilestoneForm.test.tsx` | Submit empty form | Error messages for title, description, target_date |
| Calls onSubmit with valid data | `web/tests/MilestoneForm.test.tsx` | Fill and submit valid form | onSubmit called with correct MilestoneCreate object |
| Populates edit mode | `web/tests/MilestoneForm.test.tsx` | Pass existing milestone | Form pre-filled with milestone data |
| Shows loading skeleton | `web/tests/DashboardStats.test.tsx` | isLoading=true | Skeleton placeholders displayed |
| Returns null when no stats | `web/tests/DashboardStats.test.tsx` | stats=null | Component returns null (no render) |
| Displays stats correctly | `web/tests/DashboardStats.test.tsx` | Pass valid stats object | All stat cards show correct values |
| Shows percentage for completed | `web/tests/DashboardStats.test.tsx` | stats with total>0 | Completed card shows percentage |
| Renders upcoming deadlines | `web/tests/DashboardStats.test.tsx` | stats with upcoming_deadlines | Deadline list displayed |
| Status: A Fazer | `web/tests/StatusBadge.test.tsx` | variant="status", value="A Fazer" | Gray background and text |
| Status: Em Progresso | `web/tests/StatusBadge.test.tsx` | variant="status", value="Em Progresso" | Amber background and text |
| Status: Concluída | `web/tests/StatusBadge.test.tsx` | variant="status", value="Concluída" | Green background and text |
| Status: Bloqueada | `web/tests/StatusBadge.test.tsx` | variant="status", value="Bloqueada" | Red background and text |
| Priority: Baixa | `web/tests/StatusBadge.test.tsx` | variant="priority", value="Baixa" | Light gray badge |
| Priority: Crítica | `web/tests/StatusBadge.test.tsx` | variant="priority", value="Crítica" | Red badge |
| Category variant | `web/tests/StatusBadge.test.tsx` | variant="category", value="RSL" | Purple badge |
| Does not render when closed | `web/tests/Modal.test.tsx` | isOpen=false | Modal not in DOM |
| Renders when open | `web/tests/Modal.test.tsx` | isOpen=true | Modal visible with title |
| Closes on ESC key | `web/tests/Modal.test.tsx` | Press Escape key | onClose called |
| Closes on backdrop click | `web/tests/Modal.test.tsx` | Click outside modal | onClose called |
| Does not close on content click | `web/tests/Modal.test.tsx` | Click inside modal | onClose not called |
| Renders children | `web/tests/Modal.test.tsx` | Pass child content | Children visible inside modal |

### Test Execution Commands (Deferred)

```bash
# Backend tests
poetry run pytest tests/ -v

# Frontend tests
cd web && npm run test:run
```

### Coverage Targets

- Target coverage: 100% (per AGENTS.md)
- Modules that need coverage: All frontend components (TaskForm, MilestoneForm, DashboardStats, StatusBadge, Modal)

### Known Test Dependencies

- Fixtures needed: None (use React Testing Library's built-in utilities)
- Mock requirements: Mock window/document for Modal component tests (ESC key handling)

## Notes

- Do NOT run tests — only create the plan
- Write what tests should exist, not the test results
- Based on SPEC.md section 4: "Create Component Unit Tests"
