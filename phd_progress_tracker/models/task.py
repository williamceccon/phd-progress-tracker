"""
Modelos de dados para tarefas e marcos da PhD.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from enum import Enum


class TaskStatus(Enum):
    """Status possíveis de uma tarefa."""

    TODO = "A Fazer"
    IN_PROGRESS = "Em Progresso"
    COMPLETED = "Concluída"
    BLOCKED = "Bloqueada"


class TaskPriority(Enum):
    """Prioridade das tarefas."""

    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"
    CRITICAL = "Crítica"


@dataclass
class Task:
    """
    Representa uma tarefa da PhD.

    Attributes:
        id: Identificador único da tarefa
        title: Título da tarefa
        description: Descrição detalhada
        deadline: Data limite para conclusão
        status: Status atual da tarefa
        priority: Prioridade da tarefa
        category: Categoria (ex: "Coleta de Dados", "Análise", "Escrita")
        created_at: Data de criação
        completed_at: Data de conclusão (se concluída)
    """

    id: str
    title: str
    description: str
    deadline: date
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    category: str = "Geral"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def days_remaining(self) -> int:
        """Retorna dias restantes até o deadline."""
        delta = self.deadline - date.today()
        return delta.days

    def is_overdue(self) -> bool:
        """Verifica se tarefa está atrasada."""
        return self.days_remaining() < 0 and self.status != TaskStatus.COMPLETED

    def complete(self) -> None:
        """Marca tarefa como concluída."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def to_dict(self) -> dict:
        """Converte tarefa para dicionário (para JSON)."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat(),
            "status": self.status.name,
            "priority": self.priority.name,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Cria tarefa a partir de dicionário."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            deadline=date.fromisoformat(data["deadline"]),
            status=TaskStatus[data["status"]],
            priority=TaskPriority[data["priority"]],
            category=data["category"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=(
                datetime.fromisoformat(data["completed_at"])
                if data["completed_at"]
                else None
            ),
        )
