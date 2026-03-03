"""
Task API routes.
"""

import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from phd_progress_tracker.api.schemas import TaskCreate, TaskUpdate, TaskResponse
from phd_progress_tracker.models.task import Task, TaskStatus
from phd_progress_tracker.utils.database import Database

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_db() -> Database:
    """
    Dependency to get database instance.
    For production, this should use a singleton or connection pool.
    """
    db = Database()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=List[TaskResponse])
def list_tasks(db: Database = Depends(get_db)):
    """List all tasks."""
    tasks = db.load_tasks()
    return tasks


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Database = Depends(get_db)):
    """Create a new task."""
    # Generate unique ID
    task_id = str(uuid.uuid4())

    # Create new task
    task = Task(
        id=task_id,
        title=task_data.title,
        description=task_data.description,
        deadline=task_data.deadline,
        status=TaskStatus.TODO,
        priority=task_data.priority,
        category=task_data.category,
        created_at=datetime.now(),
    )

    # Save to database
    tasks = db.load_tasks()
    tasks.append(task)
    db.save_tasks(tasks)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Database = Depends(get_db)):
    """Get a single task by ID."""
    tasks = db.load_tasks()
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate, db: Database = Depends(get_db)):
    """Update an existing task."""
    tasks = db.load_tasks()

    # Find task
    task = None
    for t in tasks:
        if t.id == task_id:
            task = t
            break

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.deadline is not None:
        task.deadline = task_data.deadline
    if task_data.status is not None:
        task.status = task_data.status
        # Auto-set completed_at when status changes to COMPLETED
        if task_data.status == TaskStatus.COMPLETED and task.completed_at is None:
            task.completed_at = datetime.now()
        elif task_data.status != TaskStatus.COMPLETED:
            task.completed_at = None
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.category is not None:
        task.category = task_data.category

    # Save changes
    db.save_tasks(tasks)

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str, db: Database = Depends(get_db)):
    """Delete a task."""
    tasks = db.load_tasks()

    # Find and remove task
    task = None
    for t in tasks:
        if t.id == task_id:
            task = t
            break

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(task)
    db.save_tasks(tasks)

    return None
