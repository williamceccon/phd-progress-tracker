from datetime import date, timedelta
import pytest
from phd_progress_tracker.utils.date_helper import (
    parse_date_input,
    format_days_remaining,
)


@pytest.fixture
def today_date():
    """Retorna a data de hoje."""
    return date.today()


def test_parse_date_input_valid_date(today_date):
    """Verifica parse_date_input com datas válidas (YYYY-MM-DD e DD/MM/YYYY)."""
    assert parse_date_input("2026-01-15") == date(2026, 1, 15)
    assert parse_date_input("15/01/2026") == date(2026, 1, 15)
    assert parse_date_input("15-01-2026") == date(2026, 1, 15)


def test_parse_date_input_relative_date(today_date):
    """Verifica parse_date_input com formato relativo (+7d, +30d, hoje, amanha)."""
    assert parse_date_input("+7d") == today_date + timedelta(days=7)
    assert parse_date_input("+30d") == today_date + timedelta(days=30)
    assert parse_date_input("hoje") == today_date
    assert parse_date_input("amanha") == today_date + timedelta(days=1)


def test_parse_date_input_invalid_date():
    """Verifica parse_date_input com data inválida deve levantar ValueError."""
    with pytest.raises(ValueError, match="Formato de data inválido"):
        parse_date_input("data invalida")
    with pytest.raises(ValueError, match="Formato de data inválido"):
        parse_date_input("2026-99-99")


@pytest.mark.parametrize(
    "days, expected_text, expected_color",
    [
        (-5, "Atrasado há 5 dias", "red"),
        (0, "Hoje!", "yellow"),
        (1, "Amanhã", "yellow"),
        (3, "3 dias (urgente)", "orange1"),
        (7, "7 dias (urgente)", "orange1"),
        (15, "15 dias", "yellow"),
        (30, "30 dias", "yellow"),
        (31, "31 dias", "green"),
    ],
)
def test_format_days_remaining(days, expected_text, expected_color):
    """Verifica format_days_remaining com dias positivos, negativos e zero."""
    text, color = format_days_remaining(days)
    assert text == expected_text
    assert color == expected_color
