"""
Tests for Dashboard API endpoints.
"""

from datetime import date, datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from phd_progress_tracker.api.main import app
from phd_progress_tracker.models.task import Task, TaskStatus, TaskPriority


@pytest.fixture
def mock_db():
    """Create a mock database."""
    mock = MagicMock()
    mock.load_tasks.return_value = []
    return mock


@pytest.fixture
def client(mock_db):
    """Create test client with mocked database."""
    with patch("phd_progress_tracker.api.routes.dashboard.Database") as MockDB:
        MockDB.return_value = mock_db
        with TestClient(app) as test_client:
            yield test_client, mock_db


class TestDashboard:
    """Tests for GET /dashboard endpoint."""

    def test_dashboard_empty(self, client):
        """Test dashboard with no tasks."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []

        response = test_client.get("/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 0
        assert data["completed_tasks"] == 0
        assert data["pending_tasks"] == 0
        assert data["overdue_tasks"] == 0
        assert data["upcoming_deadlines"] == []

    def test_dashboard_with_completed_tasks(self, client):
        """Test dashboard with completed tasks."""
        test_client, mock_db = client
        task = Task(
            id="1",
            title="Completed Task",
            description="Description",
            deadline=date.today() - timedelta(days=5),
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now() - timedelta(days=10),
            completed_at=datetime.now() - timedelta(days=2),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 1
        assert data["completed_tasks"] == 1
        assert data["pending_tasks"] == 0

    def test_dashboard_with_pending_tasks(self, client):
        """Test dashboard with pending tasks."""
        test_client, mock_db = client
        task = Task(
            id="1",
            title="Pending Task",
            description="Description",
            deadline=date.today() + timedelta(days=5),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 1
        assert data["completed_tasks"] == 0
        assert data["pending_tasks"] == 1

    def test_dashboard_with_overdue_tasks(self, client):
        """Test dashboard with overdue tasks."""
        test_client, mock_db = client
        task = Task(
            id="1",
            title="Overdue Task",
            description="Description",
            deadline=date.today() - timedelta(days=5),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now() - timedelta(days=10),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 1
        assert data["overdue_tasks"] == 1

    def test_dashboard_with_upcoming_deadlines(self, client):
        """Test dashboard with upcoming deadlines."""
        test_client, mock_db = client
        # Task with deadline in next 3 days
        task = Task(
            id="1",
            title="Upcoming Task",
            description="Description",
            deadline=date.today() + timedelta(days=3),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert len(data["upcoming_deadlines"]) == 1
        assert data["upcoming_deadlines"][0]["title"] == "Upcoming Task"

    def test_dashboard_excludes_completed_from_upcoming(self, client):
        """Test that completed tasks are excluded from upcoming deadlines."""
        test_client, mock_db = client
        # Completed task with upcoming deadline
        task = Task(
            id="1",
            title="Completed Upcoming",
            description="Description",
            deadline=date.today() + timedelta(days=3),
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
            completed_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/dashboard")

        assert response.status_code == 200
        data = response.json()
        # Completed tasks should not appear in upcoming deadlines
        assert len(data["upcoming_deadlines"]) == 0


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root(self):
        """Test root endpoint returns API info."""
        with TestClient(app) as client:
            response = client.get("/")

            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "docs" in data


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self):
        """Test health check endpoint."""
        with TestClient(app) as client:
            response = client.get("/health")

            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
