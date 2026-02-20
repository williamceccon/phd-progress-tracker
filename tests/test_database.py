import json
from datetime import date, timedelta

import pytest

from phd_progress_tracker.models.milestone import Milestone
from phd_progress_tracker.models.task import Task, TaskPriority, TaskStatus
from phd_progress_tracker.utils.database import Database


@pytest.fixture
def sample_task():
    """Uma instância de Task para testes."""
    return Task(
        id="task-001",
        title="Escrever Capítulo 1",
        description="Rascunhar primeiro capítulo",
        deadline=date.today() + timedelta(days=7),
        category="Escrita",
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
    )


@pytest.fixture
def sample_tasks(sample_task):
    """Lista de tarefas para testes."""
    task2 = Task(
        id="task-002",
        title="Revisar Literatura",
        description="Revisar artigos recentes",
        deadline=date.today() + timedelta(days=14),
        category="Pesquisa",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.MEDIUM,
    )
    return [sample_task, task2]


@pytest.fixture
def sample_milestone():
    """Uma instância de Milestone para testes."""
    return Milestone(
        id="milestone-001",
        title="Qualificação",
        description="Apresentação de qualificação",
        target_date=date.today() + timedelta(days=30),
        is_achieved=False,
    )


@pytest.fixture
def sample_milestones(sample_milestone):
    """Lista de milestones para testes."""
    milestone2 = Milestone(
        id="milestone-002",
        title="Defesa",
        description="Defesa da tese",
        target_date=date.today() + timedelta(days=180),
        is_achieved=False,
    )
    return [sample_milestone, milestone2]


@pytest.fixture
def database(tmp_path):
    """Instância de Database com diretório temporário."""
    return Database(data_dir=str(tmp_path))


def test_load_tasks_empty_file(database):
    """Verifica que load_tasks retorna lista vazia quando arquivo não existe."""
    tasks = database.load_tasks()
    assert tasks == []


def test_load_tasks_with_saved_tasks(database, sample_tasks):
    """Verifica que load_tasks carrega tarefas corretamente do arquivo JSON."""
    database.save_tasks(sample_tasks)
    tasks = database.load_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == "task-001"
    assert tasks[0].title == "Escrever Capítulo 1"
    assert tasks[0].status == TaskStatus.TODO
    assert tasks[0].priority == TaskPriority.HIGH
    assert tasks[1].id == "task-002"
    assert tasks[1].status == TaskStatus.IN_PROGRESS


def test_save_tasks(database, sample_tasks):
    """Verifica que save_tasks salva corretamente as tarefas em JSON."""
    database.save_tasks(sample_tasks)

    assert database.tasks_file.exists()

    with open(database.tasks_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["id"] == "task-001"
    assert data[0]["title"] == "Escrever Capítulo 1"
    assert data[0]["status"] == "TODO"
    assert data[0]["priority"] == "HIGH"


def test_save_and_load_tasks_roundtrip(database, sample_tasks):
    """Verifica roundtrip completo: save + load preserva dados."""
    database.save_tasks(sample_tasks)
    loaded_tasks = database.load_tasks()

    assert len(loaded_tasks) == len(sample_tasks)
    for original, loaded in zip(sample_tasks, loaded_tasks):
        assert loaded.id == original.id
        assert loaded.title == original.title
        assert loaded.description == original.description
        assert loaded.deadline == original.deadline
        assert loaded.status == original.status
        assert loaded.priority == original.priority
        assert loaded.category == original.category


def test_load_milestones_empty_file(database):
    """Verifica que load_milestones retorna lista vazia quando arquivo não existe."""
    milestones = database.load_milestones()
    assert milestones == []


def test_load_milestones_with_saved_milestones(database, sample_milestones):
    """Verifica que load_milestones carrega milestones corretamente do arquivo JSON."""
    database.save_milestones(sample_milestones)
    milestones = database.load_milestones()

    assert len(milestones) == 2
    assert milestones[0].id == "milestone-001"
    assert milestones[0].title == "Qualificação"
    assert milestones[0].is_achieved is False
    assert milestones[1].id == "milestone-002"
    assert milestones[1].title == "Defesa"


def test_save_milestones(database, sample_milestones):
    """Verifica que save_milestones salva corretamente os milestones em JSON."""
    database.save_milestones(sample_milestones)

    assert database.milestones_file.exists()

    with open(database.milestones_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["id"] == "milestone-001"
    assert data[0]["title"] == "Qualificação"
    assert data[0]["is_achieved"] is False


def test_save_and_load_milestones_roundtrip(database, sample_milestones):
    """Verifica roundtrip completo: save + load preserva dados."""
    database.save_milestones(sample_milestones)
    loaded_milestones = database.load_milestones()

    assert len(loaded_milestones) == len(sample_milestones)
    for original, loaded in zip(sample_milestones, loaded_milestones):
        assert loaded.id == original.id
        assert loaded.title == original.title
        assert loaded.description == original.description
        assert loaded.target_date == original.target_date
        assert loaded.is_achieved == original.is_achieved


def test_database_creates_data_directory(tmp_path):
    """Verifica que Database cria diretório se não existir."""
    db = Database(data_dir=str(tmp_path / "new_data_dir"))
    assert db.data_dir.exists()
    assert db.data_dir.is_dir()
