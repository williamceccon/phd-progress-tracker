"""
Milestone API routes.
"""

import uuid
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from phd_progress_tracker.api.schemas import (
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneResponse,
)
from phd_progress_tracker.models.milestone import Milestone
from phd_progress_tracker.utils.database import Database

router = APIRouter(prefix="/milestones", tags=["milestones"])


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


@router.get("", response_model=List[MilestoneResponse])
def list_milestones(db: Database = Depends(get_db)):
    """List all milestones."""
    milestones = db.load_milestones()
    return milestones


@router.post("", response_model=MilestoneResponse, status_code=201)
def create_milestone(milestone_data: MilestoneCreate, db: Database = Depends(get_db)):
    """Create a new milestone."""
    # Generate unique ID
    milestone_id = str(uuid.uuid4())

    # Create new milestone
    milestone = Milestone(
        id=milestone_id,
        title=milestone_data.title,
        description=milestone_data.description,
        target_date=milestone_data.target_date,
        is_achieved=False,
    )

    # Save to database
    milestones = db.load_milestones()
    milestones.append(milestone)
    db.save_milestones(milestones)

    return milestone


@router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_milestone(milestone_id: str, db: Database = Depends(get_db)):
    """Get a single milestone by ID."""
    milestones = db.load_milestones()
    for milestone in milestones:
        if milestone.id == milestone_id:
            return milestone
    raise HTTPException(status_code=404, detail="Milestone not found")


@router.patch("/{milestone_id}", response_model=MilestoneResponse)
def update_milestone(
    milestone_id: str,
    milestone_data: MilestoneUpdate,
    db: Database = Depends(get_db),
):
    """Update an existing milestone."""
    milestones = db.load_milestones()

    # Find milestone
    milestone = None
    for m in milestones:
        if m.id == milestone_id:
            milestone = m
            break

    if milestone is None:
        raise HTTPException(status_code=404, detail="Milestone not found")

    # Update fields
    if milestone_data.title is not None:
        milestone.title = milestone_data.title
    if milestone_data.description is not None:
        milestone.description = milestone_data.description
    if milestone_data.target_date is not None:
        milestone.target_date = milestone_data.target_date
    if milestone_data.is_achieved is not None:
        milestone.is_achieved = milestone_data.is_achieved

    # Save changes
    db.save_milestones(milestones)

    return milestone


@router.delete("/{milestone_id}", status_code=204)
def delete_milestone(milestone_id: str, db: Database = Depends(get_db)):
    """Delete a milestone."""
    milestones = db.load_milestones()

    # Find and remove milestone
    milestone = None
    for m in milestones:
        if m.id == milestone_id:
            milestone = m
            break

    if milestone is None:
        raise HTTPException(status_code=404, detail="Milestone not found")

    milestones.remove(milestone)
    db.save_milestones(milestones)

    return None
