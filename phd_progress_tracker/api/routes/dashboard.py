"""
Dashboard API routes.
"""

from datetime import date, timedelta

from fastapi import APIRouter, Depends

from phd_progress_tracker.api.schemas import DashboardResponse
from phd_progress_tracker.models.task import TaskStatus
from phd_progress_tracker.utils.database import Database

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


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


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Database = Depends(get_db)):
    """Get dashboard statistics."""
    tasks = db.load_tasks()

    # Calculate statistics
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
    pending_tasks = sum(1 for t in tasks if t.status != TaskStatus.COMPLETED)
    overdue_tasks = sum(1 for t in tasks if t.is_overdue())

    # Get upcoming deadlines (next 7 days)
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    upcoming_deadlines = [
        t
        for t in tasks
        if (
            t.status != TaskStatus.COMPLETED
            and t.deadline <= seven_days_later
            and t.deadline >= today
        )
    ]
    # Sort by deadline
    upcoming_deadlines.sort(key=lambda t: t.deadline)

    return DashboardResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        upcoming_deadlines=upcoming_deadlines,
    )
