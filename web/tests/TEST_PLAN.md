# Test Plan - Web Frontend v2.0

## Overview

This document outlines the manual usability test plan for the PhD Progress Tracker web frontend. These tests are designed to verify the application's functionality from a user's perspective.

## Test Environment

- **Frontend URL**: http://localhost:3000
- **Backend URL**: http://localhost:8000
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)
- **Viewport Sizes**:
  - Mobile: 375px
  - Tablet: 768px
  - Desktop: 1280px

---

## Dashboard Tests

### D1: Dashboard Load
**Objective**: Verify dashboard loads correctly and displays statistics.

**Steps**:
1. Open the application
2. Navigate to the dashboard (home page)
3. Verify the dashboard statistics cards are displayed
4. Check that total tasks, completed, pending, and overdue counts are visible

**Expected Result**: Dashboard loads within 2 seconds with all statistics displayed.

### D2: Stats Update After Task Creation
**Objective**: Verify dashboard stats update when a new task is created.

**Steps**:
1. Create a new task via the Tasks page
2. Return to the dashboard
3. Verify the total tasks count increased by 1

**Expected Result**: Total tasks count reflects the newly created task.

### D3: Stats Update After Task Deletion
**Objective**: Verify dashboard stats update when a task is deleted.

**Steps**:
1. Delete an existing task
2. Return to the dashboard
3. Verify the total tasks count decreased by 1

**Expected Result**: Total tasks count reflects the deleted task.

---

## Tasks Tests

### T1: Create New Task
**Objective**: Verify task creation works correctly.

**Steps**:
1. Navigate to the Tasks page
2. Click "Adicionar Tarefa" button
3. Fill in the form:
   - Title: "Test Task"
   - Description: "Test Description"
   - Deadline: Select a future date
   - Category: Select "Geral"
   - Priority: Select "Média"
4. Click "Criar" button
5. Verify the new task appears in the task list

**Expected Result**: Task is created and appears in the list with correct data.

### T2: Edit Task
**Objective**: Verify task editing works correctly.

**Steps**:
1. Click the edit button on an existing task
2. Modify the title and/or description
3. Click "Salvar" button
4. Verify the task is updated in the list

**Expected Result**: Task modifications are saved and displayed.

### T3: Complete Task
**Objective**: Verify task completion works correctly.

**Steps**:
1. Find a task with status "A Fazer"
2. Click the completion button (checkmark)
3. Verify the status changes to "Concluída"
4. Verify the task shows completion timestamp

**Expected Result**: Task status changes to "Concluída" and completion time is recorded.

### T4: Delete Task
**Objective**: Verify task deletion works correctly.

**Steps**:
1. Click the delete button on an existing task
2. Confirm the deletion in the dialog
3. Verify the task is removed from the list

**Expected Result**: Task is permanently deleted and no longer appears in the list.

### T5: Task Form Validation
**Objective**: Verify form validation prevents empty submissions.

**Steps**:
1. Click "Adicionar Tarefa"
2. Leave all required fields empty
3. Click "Criar"
4. Verify validation error messages appear

**Expected Result**: Error messages display for required fields: title, description, deadline.

---

## Milestones Tests

### M1: Create New Milestone
**Objective**: Verify milestone creation works correctly.

**Steps**:
1. Navigate to the Milestones page
2. Click "Adicionar Marco" button
3. Fill in the form:
   - Title: "Test Milestone"
   - Description: "Test Milestone Description"
   - Target Date: Select a future date
4. Click "Criar" button
5. Verify the new milestone appears in the list

**Expected Result**: Milestone is created and appears in the list with correct data.

### M2: Edit Milestone
**Objective**: Verify milestone editing works correctly.

**Steps**:
1. Click the edit button on an existing milestone
2. Modify the title and/or description
3. Click "Salvar" button
4. Verify the milestone is updated in the list

**Expected Result**: Milestone modifications are saved and displayed.

### M3: Mark Milestone as Achieved
**Objective**: Verify marking milestones as achieved works correctly.

**Steps**:
1. Find a milestone that is not yet achieved
2. Click the checkbox to mark it as achieved
3. Verify the milestone shows as achieved with checkmark
4. Verify the visual styling changes (e.g., strikethrough)

**Expected Result**: Milestone is marked as achieved with visual feedback.

### M4: Delete Milestone
**Objective**: Verify milestone deletion works correctly.

**Steps**:
1. Click the delete button on an existing milestone
2. Confirm the deletion in the dialog
3. Verify the milestone is removed from the list

**Expected Result**: Milestone is permanently deleted and no longer appears in the list.

---

## Edge Cases

### E1: Empty Task List
**Objective**: Verify empty state displays correctly.

**Steps**:
1. Delete all existing tasks
2. Navigate to the Tasks page
3. Verify the empty state message appears

**Expected Result**: "Nenhum marco encontrado" message displays with helpful guidance.

### E2: Empty Milestone List
**Objective**: Verify empty state displays correctly.

**Steps**:
1. Delete all existing milestones
2. Navigate to the Milestones page
3. Verify the empty state message appears

**Expected Result**: "Nenhum marco encontrado" message displays with helpful guidance.

### E3: Form Validation
**Objective**: Verify form validation works for milestones.

**Steps**:
1. Click "Adicionar Marco"
2. Leave all required fields empty
3. Click "Criar"
4. Verify validation error messages appear

**Expected Result**: Error messages display for required fields: title, description, target_date.

### E4: API Offline Handling
**Objective**: Verify the application handles offline scenarios gracefully.

**Steps**:
1. Stop the backend server
2. Try to create a new task
3. Verify an error message appears

**Expected Result**: User-friendly error message indicates API is unavailable.

---

## Responsive Tests

### R1: Mobile View
**Objective**: Verify application works on mobile devices.

**Steps**:
1. Set viewport to 375px width
2. Navigate through all pages
3. Verify content is readable and usable
4. Test navigation menu works

**Expected Result**: All features are accessible and readable on mobile.

### R2: Tablet View
**Objective**: Verify application works on tablet devices.

**Steps**:
1. Set viewport to 768px width
2. Navigate through all pages
3. Verify layout adapts correctly

**Expected Result**: Layout adapts properly with good use of screen space.

### R3: Desktop View
**Objective**: Verify application works on desktop devices.

**Steps**:
1. Set viewport to 1280px width
2. Navigate through all pages
3. Verify full layout is displayed

**Expected Result**: All features display with optimal desktop layout.

---

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | Required |
| Firefox | Latest | Required |
| Safari | Latest | Required |
| Edge | Latest | Required |

---

## Test Execution Checklist

- [ ] All Dashboard tests pass
- [ ] All Tasks tests pass
- [ ] All Milestones tests pass
- [ ] All Edge case tests pass
- [ ] All Responsive tests pass
- [ ] No console errors in any browser
- [ ] All forms validate correctly
- [ ] API error handling works gracefully
