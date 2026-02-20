import pytest
from typer.testing import CliRunner

from phd_progress_tracker.main import app


@pytest.fixture
def runner():
    """Runner para testar CLI."""
    return CliRunner()


def test_app_initializes():
    """Verifica que o app Typer é inicializado corretamente."""
    from typer import Typer

    assert app is not None
    assert isinstance(app, Typer)


def test_hello_command(runner):
    """Verifica que o comando hello funciona corretamente."""
    result = runner.invoke(app, ["hello", "--name", "Maria"])

    assert result.exit_code == 0
    assert "Hello Maria!" in result.stdout


def test_hello_command_default_name(runner):
    """Verifica que o comando hello usa nome padrão."""
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "Hello World!" in result.stdout
