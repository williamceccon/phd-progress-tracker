"""Entry point principal do PhD Progress Tracker."""
import typer
from phd_progress_tracker.cli.commands import app as cli_app

app = typer.Typer()


@app.command("hello")
def hello(name: str = "World"):
    """Comando de teste."""
    typer.echo(f"Hello {name}!")


# Adicionar comandos do CLI
app.add_typer(cli_app, name="")


@app.callback()
def main():
    """PhD Progress Tracker - Gerenciador de tarefas."""
    pass


if __name__ == "__main__":
    app()
