import json
from datetime import date, timedelta
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from phd_progress_tracker.cli import commands
from phd_progress_tracker.models.task import Task, TaskStatus, TaskPriority
from phd_progress_tracker.models.milestone import Milestone
from phd_progress_tracker.utils.database import Database


@pytest.fixture
def runner():
    """Runner para testar CLI."""
    return CliRunner()


@pytest.fixture
def temp_db(tmp_path):
    """Database com diretório temporário."""
    return Database(data_dir=str(tmp_path))


@pytest.fixture
def db_module(monkeypatch, temp_db):
    """Substitui o db global em commands.py pelo temporário."""
    monkeypatch.setattr(commands, "db", temp_db)
    return temp_db


@pytest.fixture
def sample_task_data():
    """Dados base para criar tarefa."""
    return {
        "id": "test-001",
        "title": "Tarefa Teste",
        "description": "Descrição de teste",
        "deadline": date.today() + timedelta(days=7),
        "category": "Teste",
        "status": TaskStatus.TODO,
        "priority": TaskPriority.MEDIUM,
    }


@pytest.fixture
def saved_task(db_module, sample_task_data):
    """Cria e salva uma tarefa no banco temporário."""
    task = Task(**sample_task_data)
    tasks = db_module.load_tasks()
    tasks.append(task)
    db_module.save_tasks(tasks)
    return task


@pytest.fixture
def saved_milestone(db_module):
    """Cria e salva um marco no banco temporário."""
    milestone = Milestone(
        id="mile-001",
        title="Qualificação",
        description="Apresentação de qualificação",
        target_date=date.today() + timedelta(days=30),
        is_achieved=False,
    )
    milestones = db_module.load_milestones()
    milestones.append(milestone)
    db_module.save_milestones(milestones)
    return milestone


class TestAddCommand:
    """Testes para o comando 'add'."""

    def test_add_task_success(self, runner, db_module):
        """Verifica adição de tarefa com sucesso."""
        result = runner.invoke(
            commands.app,
            [
                "add",
                "Nova Tarefa",
                "--deadline",
                "2026-03-01",
                "--category",
                "Pesquisa",
            ],
        )

        assert result.exit_code == 0
        assert "adicionada com sucesso" in result.stdout
        tasks = db_module.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Nova Tarefa"

    def test_add_task_with_relative_deadline(self, runner, db_module):
        """Verifica adição com prazo relativo (+14d)."""
        result = runner.invoke(
            commands.app,
            ["add", "Tarefa Relativa", "--deadline", "+14d"],
        )

        assert result.exit_code == 0
        tasks = db_module.load_tasks()
        assert len(tasks) == 1
        expected_deadline = date.today() + timedelta(days=14)
        assert tasks[0].deadline == expected_deadline

    def test_add_task_with_priority(self, runner, db_module):
        """Verifica adição com prioridade."""
        result = runner.invoke(
            commands.app,
            [
                "add",
                "Tarefa Alta Prioridade",
                "--deadline",
                "2026-04-01",
                "--priority",
                "HIGH",
            ],
        )

        assert result.exit_code == 0
        tasks = db_module.load_tasks()
        assert tasks[0].priority == TaskPriority.HIGH

    def test_add_task_invalid_priority(self, runner, db_module):
        """Verifica erro com prioridade inválida."""
        result = runner.invoke(
            commands.app,
            [
                "add",
                "Tarefa Inválida",
                "--deadline",
                "2026-04-01",
                "--priority",
                "INVALID",
            ],
        )

        assert result.exit_code == 1

    def test_add_task_invalid_deadline(self, runner, db_module):
        """Verifica erro com deadline inválida."""
        result = runner.invoke(
            commands.app,
            ["add", "Tarefa Inválida", "--deadline", "data-invalida"],
        )

        assert result.exit_code == 1


class TestListCommand:
    """Testes para o comando 'list'."""

    def test_list_tasks_empty(self, runner, db_module):
        """Verifica listagem vazia."""
        result = runner.invoke(commands.app, ["list"])

        assert result.exit_code == 0
        assert "Nenhuma tarefa encontrada" in result.stdout

    def test_list_tasks_with_data(self, runner, saved_task):
        """Verifica listagem com tarefas."""
        result = runner.invoke(commands.app, ["list"])

        assert result.exit_code == 0
        assert "Tarefa Teste" in result.stdout

    def test_list_tasks_filter_by_status(self, runner, saved_task):
        """Verifica filtro por status."""
        result = runner.invoke(commands.app, ["list", "--status", "TODO"])

        assert result.exit_code == 0
        assert "Tarefa Teste" in result.stdout

    def test_list_tasks_filter_by_category(self, runner, saved_task):
        """Verifica filtro por categoria."""
        result = runner.invoke(commands.app, ["list", "--category", "Teste"])

        assert result.exit_code == 0
        assert "Tarefa Teste" in result.stdout


class TestEditCommand:
    """Testes para o comando 'edit'."""

    def test_edit_task_success_title(self, runner, saved_task):
        """Verifica edição de título."""
        result = runner.invoke(
            commands.app,
            ["edit", saved_task.id, "--title", "Título Editado"],
        )

        assert result.exit_code == 0
        assert "atualizada com sucesso" in result.stdout

    def test_edit_task_success_deadline(self, runner, saved_task):
        """Verifica edição de prazo."""
        result = runner.invoke(
            commands.app,
            ["edit", saved_task.id, "--deadline", "+30d"],
        )

        assert result.exit_code == 0
        assert "atualizada com sucesso" in result.stdout

    def test_edit_task_not_found(self, runner, db_module):
        """Verifica erro ao editar tarefa inexistente."""
        result = runner.invoke(
            commands.app,
            ["edit", "id-inexistente", "--title", "Novo Título"],
        )

        assert result.exit_code == 1
        assert "não encontrada" in result.stdout

    def test_edit_task_no_fields(self, runner, saved_task):
        """Verifica erro ao não fornecer campos."""
        result = runner.invoke(
            commands.app,
            ["edit", saved_task.id],
        )

        assert result.exit_code == 0
        assert "Nenhum campo para atualizar" in result.stdout

    def test_edit_task_invalid_deadline(self, runner, saved_task):
        """Verifica erro com deadline inválida."""
        result = runner.invoke(
            commands.app,
            ["edit", saved_task.id, "--deadline", "data-invalida"],
        )

        assert result.exit_code == 1


class TestCompleteCommand:
    """Testes para o comando 'complete'."""

    def test_complete_task_success(self, runner, saved_task):
        """Verifica conclusão de tarefa."""
        result = runner.invoke(
            commands.app,
            ["complete", saved_task.id],
        )

        assert result.exit_code == 0
        assert "concluída" in result.stdout

    def test_complete_task_not_found(self, runner, db_module):
        """Verifica erro ao completar tarefa inexistente."""
        result = runner.invoke(
            commands.app,
            ["complete", "id-inexistente"],
        )

        assert result.exit_code == 1
        assert "não encontrada" in result.stdout


class TestDashboardCommand:
    """Testes para o comando 'dashboard'."""

    def test_dashboard_empty(self, runner, db_module):
        """Verifica dashboard vazio."""
        result = runner.invoke(commands.app, ["dashboard"])

        assert result.exit_code == 0
        assert "Total de Tarefas" in result.stdout

    def test_dashboard_with_tasks(self, runner, saved_task):
        """Verifica dashboard com tarefas."""
        result = runner.invoke(commands.app, ["dashboard"])

        assert result.exit_code == 0
        assert "Tarefa Teste" in result.stdout

    def test_dashboard_with_milestones(self, runner, saved_task, saved_milestone):
        """Verifica dashboard com milestones."""
        result = runner.invoke(commands.app, ["dashboard"])

        assert result.exit_code == 0
        assert "Marcos Importantes" in result.stdout


class TestMilestoneAddCommand:
    """Testes para o comando 'milestone-add'."""

    def test_add_milestone_success(self, runner, db_module):
        """Verifica adição de marco com sucesso."""
        result = runner.invoke(
            commands.app,
            [
                "milestone-add",
                "Defesa",
                "--date",
                "2026-12-01",
                "--desc",
                "Defesa da tese",
            ],
        )

        assert result.exit_code == 0
        assert "Marco" in result.stdout and "adicionado" in result.stdout
        milestones = db_module.load_milestones()
        assert len(milestones) == 1
        assert milestones[0].title == "Defesa"

    def test_add_milestone_invalid_date(self, runner, db_module):
        """Verifica erro com data inválida."""
        result = runner.invoke(
            commands.app,
            ["milestone-add", "Defesa", "--date", "data-invalida"],
        )

        assert result.exit_code == 1
