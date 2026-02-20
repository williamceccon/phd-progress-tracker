from datetime import date, datetime, timedelta
import pytest
from phd_progress_tracker.models.task import Task, TaskPriority, TaskStatus


@pytest.fixture
def task_data():
    """Dados básicos para criar uma tarefa."""
    return {
        "id": "task-123",
        "title": "Escrever Introdução",
        "description": "Rascunhar a introdução da tese",
        "deadline": date.today() + timedelta(days=7),
        "category": "Escrita",
    }


@pytest.fixture
def sample_task(task_data):
    """Uma instância de Task com dados padrão."""
    return Task(**task_data)


@pytest.fixture
def overdue_task(task_data):
    """Uma instância de Task que está atrasada."""
    overdue_data = task_data.copy()
    overdue_data["deadline"] = date.today() - timedelta(days=1)
    return Task(**overdue_data)


@pytest.fixture
def future_task(task_data):
    """Uma instância de Task com deadline no futuro."""
    future_data = task_data.copy()
    future_data["deadline"] = date.today() + timedelta(days=10)
    return Task(**future_data)


def test_task_creation_all_fields(task_data):
    """Verifica a criação de uma tarefa com todos os campos."""
    now = datetime.now()
    task = Task(
        **task_data,
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
        created_at=now,
        completed_at=None,
    )

    assert task.id == task_data["id"]
    assert task.title == task_data["title"]
    assert task.description == task_data["description"]
    assert task.deadline == task_data["deadline"]
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.HIGH
    assert task.category == task_data["category"]
    assert task.created_at == now
    assert task.completed_at is None


def test_task_creation_default_fields(task_data):
    """Verifica a criação de uma tarefa com campos padrão."""
    task = Task(**task_data)

    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None


def test_task_edit_title(sample_task):
    """Verifica a edição do título da tarefa."""
    new_title = "Revisar Introdução"
    sample_task.title = new_title
    assert sample_task.title == new_title


def test_task_edit_deadline(sample_task):
    """Verifica a edição do prazo da tarefa."""
    new_deadline = date.today() + timedelta(days=14)
    sample_task.deadline = new_deadline
    assert sample_task.deadline == new_deadline


def test_task_complete_method(sample_task):
    """Verifica o método complete() muda o status e data de conclusão."""
    sample_task.complete()
    assert sample_task.status == TaskStatus.COMPLETED
    assert isinstance(sample_task.completed_at, datetime)


def test_task_is_overdue_true(overdue_task):
    """Verifica se is_overdue() retorna True para tarefa atrasada."""
    assert overdue_task.is_overdue() is True


def test_task_is_overdue_false_future_task(future_task):
    """Verifica se is_overdue() retorna False para tarefa futura."""
    assert future_task.is_overdue() is False


def test_task_is_overdue_false_completed_overdue(overdue_task):
    """Verifica se is_overdue() retorna False para tarefa atrasada mas concluída."""
    overdue_task.complete()
    assert overdue_task.is_overdue() is False


def test_task_days_remaining_future(future_task):
    """Verifica cálculo correto de days_remaining() para tarefa futura."""
    expected_days = (future_task.deadline - date.today()).days
    assert future_task.days_remaining() == expected_days


def test_task_days_remaining_past(overdue_task):
    """Verifica cálculo correto de days_remaining() para tarefa atrasada."""
    expected_days = (overdue_task.deadline - date.today()).days
    assert overdue_task.days_remaining() == expected_days


def test_task_days_remaining_today(task_data):
    """Verifica cálculo correto de days_remaining() para tarefa com deadline hoje."""
    task_today_data = task_data.copy()
    task_today_data["deadline"] = date.today()
    task_today = Task(**task_today_data)
    assert task_today.days_remaining() == 0


def test_task_status_enum_validation():
    """Verifica se TaskStatus possui os valores esperados."""
    assert TaskStatus.TODO.value == "A Fazer"
    assert TaskStatus.IN_PROGRESS.value == "Em Progresso"
    assert TaskStatus.COMPLETED.value == "Concluída"
    assert TaskStatus.BLOCKED.value == "Bloqueada"


def test_task_priority_enum_validation():
    """Verifica se TaskPriority possui os valores esperados."""
    assert TaskPriority.LOW.value == "Baixa"
    assert TaskPriority.MEDIUM.value == "Média"
    assert TaskPriority.HIGH.value == "Alta"
    assert TaskPriority.CRITICAL.value == "Crítica"


def test_task_to_dict_method(sample_task):
    """Verifica a conversão da tarefa para dicionário."""
    task_dict = sample_task.to_dict()
    assert isinstance(task_dict, dict)
    assert task_dict["id"] == sample_task.id
    assert task_dict["title"] == sample_task.title
    assert task_dict["deadline"] == sample_task.deadline.isoformat()
    assert task_dict["status"] == sample_task.status.name
    assert task_dict["priority"] == sample_task.priority.name
    assert task_dict["created_at"] == sample_task.created_at.isoformat()
    assert task_dict["completed_at"] is None


def test_task_from_dict_method(sample_task):
    """Verifica a criação de tarefa a partir de dicionário."""
    task_dict = sample_task.to_dict()
    new_task = Task.from_dict(task_dict)

    assert new_task.id == sample_task.id
    assert new_task.title == sample_task.title
    assert new_task.description == sample_task.description
    assert new_task.deadline == sample_task.deadline
    assert new_task.status == sample_task.status
    assert new_task.priority == sample_task.priority
    assert new_task.category == sample_task.category
    # Comparar isoformat para datetime devido a possíveis diferenças de microssegundos
    assert new_task.created_at.isoformat(
        timespec="milliseconds"
    ) == sample_task.created_at.isoformat(timespec="milliseconds")
    assert (
        new_task.completed_at.isoformat(timespec="milliseconds")
        if new_task.completed_at
        else None
    ) == (
        sample_task.completed_at.isoformat(timespec="milliseconds")
        if sample_task.completed_at
        else None
    )


def test_task_from_dict_with_completed_at(sample_task):
    """Verifica a criação de tarefa a partir de dicionário com completed_at."""
    sample_task.complete()
    task_dict = sample_task.to_dict()
    new_task = Task.from_dict(task_dict)

    assert new_task.completed_at.isoformat(
        timespec="milliseconds"
    ) == sample_task.completed_at.isoformat(timespec="milliseconds")
