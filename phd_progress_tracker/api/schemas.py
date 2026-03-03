"""
Pydantic schemas for API request/response validation.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from phd_progress_tracker.models.task import TaskPriority, TaskStatus

# Task Schemas


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str
    description: str
    deadline: date
    category: str = "Geral"
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    deadline: date
    status: TaskStatus
    priority: TaskPriority
    category: str
    created_at: datetime
    completed_at: Optional[datetime] = None


# Milestone Schemas


class MilestoneCreate(BaseModel):
    """Schema for creating a new milestone."""

    title: str
    description: str
    target_date: date


class MilestoneUpdate(BaseModel):
    """Schema for updating an existing milestone."""

    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    is_achieved: Optional[bool] = None


class MilestoneResponse(BaseModel):
    """Schema for milestone response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    target_date: date
    is_achieved: bool


# Dashboard Schema


class DashboardResponse(BaseModel):
    """Schema for dashboard statistics response."""

    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    upcoming_deadlines: list[TaskResponse]
