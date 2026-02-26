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
    """Instância de Database com diretório temporário e banco em memória."""
    return Database(data_dir=str(tmp_path), db_path=":memory:")


def test_load_tasks_empty_db(database):
    """Verifica que load_tasks retorna lista vazia quando banco está vazio."""
    tasks = database.load_tasks()
    assert tasks == []


def test_load_tasks_with_saved_tasks(database, sample_tasks):
    """Verifica que load_tasks carrega tarefas corretamente do SQLite."""
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
    """Verifica que save_tasks salva corretamente as tarefas no SQLite."""
    database.save_tasks(sample_tasks)

    # Since we're using :memory:, we verify through load_tasks
    loaded = database.load_tasks()
    assert len(loaded) == 2
    assert loaded[0].id == "task-001"
    assert loaded[0].title == "Escrever Capítulo 1"
    assert loaded[0].status == TaskStatus.TODO
    assert loaded[0].priority == TaskPriority.HIGH


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


def test_load_milestones_empty_db(database):
    """Verifica que load_milestones retorna lista vazia quando banco está vazio."""
    milestones = database.load_milestones()
    assert milestones == []


def test_load_milestones_with_saved_milestones(database, sample_milestones):
    """Verifica que load_milestones carrega milestones corretamente do SQLite."""
    database.save_milestones(sample_milestones)
    milestones = database.load_milestones()

    assert len(milestones) == 2
    assert milestones[0].id == "milestone-001"
    assert milestones[0].title == "Qualificação"
    assert milestones[0].is_achieved is False
    assert milestones[1].id == "milestone-002"
    assert milestones[1].title == "Defesa"


def test_save_milestones(database, sample_milestones):
    """Verifica que save_milestones salva corretamente os milestones no SQLite."""
    database.save_milestones(sample_milestones)

    # Verify through load
    loaded = database.load_milestones()
    assert len(loaded) == 2
    assert loaded[0].id == "milestone-001"
    assert loaded[0].title == "Qualificação"
    assert loaded[0].is_achieved is False


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
    db = Database(data_dir=str(tmp_path / "new_data_dir"), db_path=":memory:")
    assert db.data_dir.exists()
    assert db.data_dir.is_dir()


def test_migration_from_json(tmp_path, sample_tasks, sample_milestones):
    """Verifica migração de JSON para SQLite."""
    # Create JSON files (legacy format)
    import json

    tasks_file = tmp_path / "tasks.json"
    milestones_file = tmp_path / "milestones.json"

    tasks_data = [task.to_dict() for task in sample_tasks]
    milestones_data = [m.to_dict() for m in sample_milestones]

    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f)

    with open(milestones_file, "w", encoding="utf-8") as f:
        json.dump(milestones_data, f)

    # Create database - should trigger migration
    db = Database(data_dir=str(tmp_path), db_path=str(tmp_path / "test.db"))

    # Verify JSON files were moved to backup
    assert not tasks_file.exists()
    assert not milestones_file.exists()

    backup_dir = tmp_path / "json_backup"
    assert (backup_dir / "tasks.json").exists()
    assert (backup_dir / "milestones.json").exists()

    # Verify data was migrated to SQLite
    tasks = db.load_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == "task-001"

    milestones = db.load_milestones()
    assert len(milestones) == 2
    assert milestones[0].id == "milestone-001"


def test_save_tasks_clears_existing(tmp_path, sample_tasks):
    """Verifica que save_tasks limpa tarefas existentes antes de salvar."""
    db = Database(data_dir=str(tmp_path), db_path=":memory:")

    # Save initial tasks
    db.save_tasks(sample_tasks)
    assert len(db.load_tasks()) == 2

    # Save empty list - should clear all tasks
    db.save_tasks([])
    assert len(db.load_tasks()) == 0


def test_save_milestones_clears_existing(tmp_path, sample_milestones):
    """Verifica que save_milestones limpa milestones existentes antes de salvar."""
    db = Database(data_dir=str(tmp_path), db_path=":memory:")

    # Save initial milestones
    db.save_milestones(sample_milestones)
    assert len(db.load_milestones()) == 2

    # Save empty list - should clear all milestones
    db.save_milestones([])
    assert len(db.load_milestones()) == 0


def test_close_method(tmp_path):
    """Verifica que close() fecha a conexão corretamente."""
    db = Database(data_dir=str(tmp_path), db_path=":memory:")

    # Save some data to ensure connection is created
    db.save_tasks(sample_tasks_helper())

    # Verify data is there
    assert len(db.load_tasks()) == 2

    # Close the connection - should not raise any error
    db.close()

    # Connection should be None now
    assert db._connection is None


def test_context_manager(tmp_path):
    """Verifica uso do Database como context manager."""
    with Database(data_dir=str(tmp_path), db_path=":memory:") as db:
        db.save_tasks(sample_tasks_helper())
        tasks = db.load_tasks()
        assert len(tasks) == 2
    # Connection should be closed after exiting context


def test_migration_idempotent(tmp_path, sample_tasks, sample_milestones):
    """Verifica que migração não roda se dados já existem no banco."""
    import json

    # Create JSON files
    tasks_file = tmp_path / "tasks.json"
    milestones_file = tmp_path / "milestones.json"

    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in sample_tasks], f)

    with open(milestones_file, "w", encoding="utf-8") as f:
        json.dump([m.to_dict() for m in sample_milestones], f)

    # First instantiation - triggers migration
    db = Database(data_dir=str(tmp_path), db_path=str(tmp_path / "test.db"))

    # JSON files should be moved to backup
    assert not tasks_file.exists()
    assert not milestones_file.exists()

    # Get original task count
    original_count = len(db.load_tasks())

    # Recreate JSON files (simulating user re-adding them)
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in sample_tasks], f)

    # Second instantiation - should NOT trigger migration (idempotent)
    db2 = Database(data_dir=str(tmp_path), db_path=str(tmp_path / "test.db"))

    # Should still have same count (not doubled)
    assert len(db2.load_tasks()) == original_count


def sample_tasks_helper():
    """Helper para criar tarefas de exemplo."""
    from datetime import date, timedelta
    from phd_progress_tracker.models.task import Task, TaskPriority, TaskStatus

    return [
        Task(
            id="task-001",
            title="Escrever Capítulo 1",
            description="Rascunhar primeiro capítulo",
            deadline=date.today() + timedelta(days=7),
            category="Escrita",
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
        ),
        Task(
            id="task-002",
            title="Revisar Literatura",
            description="Revisar artigos recentes",
            deadline=date.today() + timedelta(days=14),
            category="Pesquisa",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.MEDIUM,
        ),
    ]
