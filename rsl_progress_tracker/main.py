"""
Entry point principal do RSL Progress Tracker.
"""

import typer
from rsl_progress_tracker.cli.commands import app
from rsl_progress_tracker import __version__


def version_callback(value: bool):
    """Callback para exibir versão."""
    if value:
        typer.echo(f"RSL Progress Tracker v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Exibe versão da aplicação",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    🎓 RSL Progress Tracker

    Gerenciador de tarefas, prazos e progresso para sua dissertação.
    """
    pass


if __name__ == "__main__":
    app()
