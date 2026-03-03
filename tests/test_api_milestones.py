"""
Tests for Milestone API endpoints.
"""

from datetime import date
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from phd_progress_tracker.api.main import app
from phd_progress_tracker.models.milestone import Milestone


@pytest.fixture
def mock_db():
    """Create a mock database."""
    mock = MagicMock()
    mock.load_milestones.return_value = []
    return mock


@pytest.fixture
def client(mock_db):
    """Create test client with mocked database."""
    with patch("phd_progress_tracker.api.routes.milestones.Database") as MockDB:
        MockDB.return_value = mock_db
        with TestClient(app) as test_client:
            yield test_client, mock_db


class TestListMilestones:
    """Tests for GET /milestones endpoint."""

    def test_list_milestones_empty(self, client):
        """Test listing milestones when database is empty."""
        test_client, mock_db = client
        mock_db.load_milestones.return_value = []

        response = test_client.get("/milestones")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_milestones_with_data(self, client):
        """Test listing milestones with existing data."""
        test_client, mock_db = client
        milestone = Milestone(
            id="1",
            title="Qualification Exam",
            description="Pass qualification exam",
            target_date=date(2025, 6, 15),
            is_achieved=False,
        )
        mock_db.load_milestones.return_value = [milestone]

        response = test_client.get("/milestones")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Qualification Exam"


class TestCreateMilestone:
    """Tests for POST /milestones endpoint."""

    def test_create_milestone_success(self, client):
        """Test creating a new milestone."""
        test_client, mock_db = client
        mock_db.load_milestones.return_value = []
        mock_db.save_milestones.return_value = None

        payload = {
            "title": "Defense",
            "description": "PhD defense",
            "target_date": "2026-01-15",
        }

        response = test_client.post("/milestones", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Defense"
        assert data["is_achieved"] is False
        mock_db.save_milestones.assert_called_once()


class TestGetMilestone:
    """Tests for GET /milestones/{id} endpoint."""

    def test_get_milestone_success(self, client):
        """Test getting a single milestone."""
        test_client, mock_db = client
        milestone = Milestone(
            id="milestone-123",
            title="Qualification Exam",
            description="Pass qualification exam",
            target_date=date(2025, 6, 15),
            is_achieved=False,
        )
        mock_db.load_milestones.return_value = [milestone]

        response = test_client.get("/milestones/milestone-123")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "milestone-123"
        assert data["title"] == "Qualification Exam"

    def test_get_milestone_not_found(self, client):
        """Test getting non-existent milestone."""
        test_client, mock_db = client
        mock_db.load_milestones.return_value = []

        response = test_client.get("/milestones/nonexistent")

        assert response.status_code == 404
        assert response.json()["detail"] == "Milestone not found"


class TestUpdateMilestone:
    """Tests for PATCH /milestones/{id} endpoint."""

    def test_update_milestone_success(self, client):
        """Test updating a milestone."""
        test_client, mock_db = client
        milestone = Milestone(
            id="milestone-123",
            title="Original Title",
            description="Original Description",
            target_date=date(2025, 6, 15),
            is_achieved=False,
        )
        mock_db.load_milestones.return_value = [milestone]
        mock_db.save_milestones.return_value = None

        payload = {"title": "Updated Title", "is_achieved": True}

        response = test_client.patch("/milestones/milestone-123", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["is_achieved"] is True

    def test_update_milestone_not_found(self, client):
        """Test updating non-existent milestone."""
        test_client, mock_db = client
        mock_db.load_milestones.return_value = []

        payload = {"title": "New Title"}

        response = test_client.patch("/milestones/nonexistent", json=payload)

        assert response.status_code == 404


class TestDeleteMilestone:
    """Tests for DELETE /milestones/{id} endpoint."""

    def test_delete_milestone_success(self, client):
        """Test deleting a milestone."""
        test_client, mock_db = client
        milestone = Milestone(
            id="milestone-123",
            title="Test Milestone",
            description="Test Description",
            target_date=date(2025, 6, 15),
            is_achieved=False,
        )
        mock_db.load_milestones.return_value = [milestone]
        mock_db.save_milestones.return_value = None

        response = test_client.delete("/milestones/milestone-123")

        assert response.status_code == 204
        mock_db.save_milestones.assert_called_once()

    def test_delete_milestone_not_found(self, client):
        """Test deleting non-existent milestone."""
        test_client, mock_db = client
        mock_db.load_milestones.return_value = []

        response = test_client.delete("/milestones/nonexistent")

        assert response.status_code == 404
