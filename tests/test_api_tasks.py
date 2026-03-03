"""
Tests for Task API endpoints.
"""

from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from phd_progress_tracker.api.main import app
from phd_progress_tracker.api.routes import tasks
from phd_progress_tracker.models.task import Task, TaskStatus, TaskPriority
from phd_progress_tracker.utils.database import Database


@pytest.fixture
def mock_db():
    """Create a mock database."""
    mock = MagicMock(spec=Database)
    mock.load_tasks.return_value = []
    mock.close.return_value = None
    return mock


@pytest.fixture
def client(mock_db):
    """Create test client with mocked database."""

    def mock_get_db():
        try:
            yield mock_db
        finally:
            pass

    app.dependency_overrides[tasks.get_db] = mock_get_db

    with TestClient(app) as test_client:
        yield test_client, mock_db

    # Clean up overrides
    app.dependency_overrides.clear()


class TestListTasks:
    """Tests for GET /tasks endpoint."""

    def test_list_tasks_empty(self, client):
        """Test listing tasks when database is empty."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []

        response = test_client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_with_data(self, client):
        """Test listing tasks with existing data."""
        test_client, mock_db = client
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            deadline=date(2025, 12, 31),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/tasks")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"


class TestCreateTask:
    """Tests for POST /tasks endpoint."""

    def test_create_task_success(self, client):
        """Test creating a new task."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []
        mock_db.save_tasks.return_value = None

        payload = {
            "title": "New Task",
            "description": "New Description",
            "deadline": "2025-12-31",
            "category": "Research",
            "priority": "Alta",  # Portuguese value
        }

        response = test_client.post("/tasks", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["status"] == "A Fazer"
        assert data["priority"] == "Alta"
        mock_db.save_tasks.assert_called_once()

    def test_create_task_with_defaults(self, client):
        """Test creating task with default values."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []
        mock_db.save_tasks.return_value = None

        payload = {
            "title": "Minimal Task",
            "description": "Description",
            "deadline": "2025-12-31",
        }

        response = test_client.post("/tasks", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["category"] == "Geral"
        assert data["priority"] == "Média"


class TestGetTask:
    """Tests for GET /tasks/{id} endpoint."""

    def test_get_task_success(self, client):
        """Test getting a single task."""
        test_client, mock_db = client
        task = Task(
            id="task-123",
            title="Test Task",
            description="Test Description",
            deadline=date(2025, 12, 31),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]

        response = test_client.get("/tasks/task-123")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "task-123"
        assert data["title"] == "Test Task"

    def test_get_task_not_found(self, client):
        """Test getting non-existent task."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []

        response = test_client.get("/tasks/nonexistent")

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


class TestUpdateTask:
    """Tests for PATCH /tasks/{id} endpoint."""

    def test_update_task_success(self, client):
        """Test updating a task."""
        test_client, mock_db = client
        task = Task(
            id="task-123",
            title="Original Title",
            description="Original Description",
            deadline=date(2025, 12, 31),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]
        mock_db.save_tasks.return_value = None

        payload = {"title": "Updated Title", "status": "Em Progresso"}

        response = test_client.patch("/tasks/task-123", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "Em Progresso"

    def test_update_task_not_found(self, client):
        """Test updating non-existent task."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []

        payload = {"title": "New Title"}

        response = test_client.patch("/tasks/nonexistent", json=payload)

        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /tasks/{id} endpoint."""

    def test_delete_task_success(self, client):
        """Test deleting a task."""
        test_client, mock_db = client
        task = Task(
            id="task-123",
            title="Test Task",
            description="Test Description",
            deadline=date(2025, 12, 31),
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            category="Geral",
            created_at=datetime.now(),
        )
        mock_db.load_tasks.return_value = [task]
        mock_db.save_tasks.return_value = None

        response = test_client.delete("/tasks/task-123")

        assert response.status_code == 204
        mock_db.save_tasks.assert_called_once()

    def test_delete_task_not_found(self, client):
        """Test deleting non-existent task."""
        test_client, mock_db = client
        mock_db.load_tasks.return_value = []

        response = test_client.delete("/tasks/nonexistent")

        assert response.status_code == 404
