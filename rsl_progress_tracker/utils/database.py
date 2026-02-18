"""
Gerenciamento de persistência de dados em JSON.
"""

import json
from pathlib import Path
from typing import List
from rsl_progress_tracker.models.task import Task
from rsl_progress_tracker.models.milestone import Milestone


class Database:
    """Gerencia persistência de tarefas e milestones."""

    def __init__(self, data_dir: str = "data"):
        """
        Inicializa database.

        Args:
            data_dir: Diretório onde dados serão salvos
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self.milestones_file = self.data_dir / "milestones.json"

    def save_tasks(self, tasks: List[Task]) -> None:
        """Salva lista de tarefas."""
        data = [task.to_dict() for task in tasks]
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_tasks(self) -> List[Task]:
        """Carrega lista de tarefas."""
        if not self.tasks_file.exists():
            return []
        with open(self.tasks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(task_data) for task_data in data]

    def save_milestones(self, milestones: List[Milestone]) -> None:
        """Salva lista de milestones."""
        data = [milestone.to_dict() for milestone in milestones]
        with open(self.milestones_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_milestones(self) -> List[Milestone]:
        """Carrega lista de milestones."""
        if not self.milestones_file.exists():
            return []
        with open(self.milestones_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Milestone.from_dict(m_data) for m_data in data]
