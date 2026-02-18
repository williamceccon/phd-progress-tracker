"""
Modelo para marcos importantes da dissertação.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Milestone:
    """
    Representa um marco importante da dissertação.

    Examples:
        - Qualificação
        - Defesa
        - Submissão de artigo
    """

    id: str
    title: str
    description: str
    target_date: date
    is_achieved: bool = False

    def days_until(self) -> int:
        """Retorna dias até o marco."""
        delta = self.target_date - date.today()
        return delta.days

    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_date": self.target_date.isoformat(),
            "is_achieved": self.is_achieved,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Milestone":
        """Cria milestone a partir de dicionário."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            target_date=date.fromisoformat(data["target_date"]),
            is_achieved=data["is_achieved"],
        )
