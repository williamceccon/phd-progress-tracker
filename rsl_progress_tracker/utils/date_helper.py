"""
Funções auxiliares para manipulação de datas.
"""

from datetime import date, timedelta
from typing import Tuple


def format_days_remaining(days: int) -> Tuple[str, str]:
    """
    Formata dias restantes com cor apropriada.

    Returns:
        Tupla (texto, cor) para exibição no Rich
    """
    if days < 0:
        return f"Atrasado há {abs(days)} dias", "red"
    elif days == 0:
        return "Hoje!", "yellow"
    elif days == 1:
        return "Amanhã", "yellow"
    elif days <= 7:
        return f"{days} dias (urgente)", "orange1"
    elif days <= 30:
        return f"{days} dias", "yellow"
    else:
        return f"{days} dias", "green"


def parse_date_input(date_str: str) -> date:
    """
    Parseia string de data em múltiplos formatos.

    Args:
        date_str: String como "2026-12-31", "31/12/2026", "hoje", "+7d"

    Returns:
        Objeto date
    """
    date_str = date_str.lower().strip()

    # Atalhos
    if date_str == "hoje":
        return date.today()
    elif date_str == "amanha" or date_str == "amanhã":
        return date.today() + timedelta(days=1)
    elif date_str.startswith("+"):
        # Formato: +7d (7 dias a partir de hoje)
        days = int(date_str[1:-1])
        return date.today() + timedelta(days=days)

    # Formatos padrão
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Formato de data inválido: {date_str}")


poe
