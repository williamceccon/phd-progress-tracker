"""
Comandos CLI para o RSL Progress Tracker.
"""

import uuid
from datetime import date
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich import box

from rsl_progress_tracker.models.task import Task, TaskStatus, TaskPriority
from rsl_progress_tracker.models.milestone import Milestone
from rsl_progress_tracker.utils.database import Database
from rsl_progress_tracker.utils.date_helper import (
    format_days_remaining,
    parse_date_input,
)

app = typer.Typer()
console = Console()
db = Database()


@app.command("add")
def add_task(
    title: str = typer.Argument(..., help="Título da tarefa"),
    description: str = typer.Option("", "--desc", "-d", help="Descrição da tarefa"),
    deadline: str = typer.Option(
        ..., "--deadline", "-dl", help="Data limite (YYYY-MM-DD ou +Nd)"
    ),
    category: str = typer.Option(
        "Geral", "--category", "-c", help="Categoria da tarefa"
    ),
    priority: str = typer.Option(
        "MEDIUM", "--priority", "-p", help="LOW, MEDIUM, HIGH, CRITICAL"
    ),
):
    """
    Adiciona nova tarefa ao tracker.

    Exemplos:
        rsl add "Revisar literatura" --deadline 2026-03-01 --category "RSL"
        rsl add "Análise de dados" --deadline +14d --priority HIGH
    """
    try:
        deadline_date = parse_date_input(deadline)
        priority_enum = TaskPriority[priority.upper()]
    except (ValueError, KeyError) as e:
        console.print(f"[red]Erro: {e}[/red]")
        raise typer.Exit(1)

    task = Task(
        id=str(uuid.uuid4())[:8],
        title=title,
        description=description,
        deadline=deadline_date,
        category=category,
        priority=priority_enum,
    )

    tasks = db.load_tasks()
    tasks.append(task)
    db.save_tasks(tasks)

    console.print(
        f"[green]✓[/green] Tarefa '{title}' adicionada com sucesso! (ID: {task.id})"
    )


@app.command("list")
def list_tasks(
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filtrar por status"
    ),
    category: Optional[str] = typer.Option(
        None, "--category", "-c", help="Filtrar por categoria"
    ),
):
    """
    Lista todas as tarefas.
    """
    tasks = db.load_tasks()

    # Filtros
    if status:
        tasks = [t for t in tasks if t.status.name == status.upper()]
    if category:
        tasks = [t for t in tasks if t.category.lower() == category.lower()]

    if not tasks:
        console.print("[yellow]Nenhuma tarefa encontrada.[/yellow]")
        return

    # Criar tabela
    table = Table(title="📋 Tarefas da RSL", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Título", style="white")
    table.add_column("Categoria", style="magenta")
    table.add_column("Prazo", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Prioridade", style="red")

    for task in sorted(tasks, key=lambda t: t.deadline):
        days_text, color = format_days_remaining(task.days_remaining())

        # Emoji por status
        status_emoji = {
            TaskStatus.TODO: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.BLOCKED: "🚫",
        }

        table.add_row(
            task.id,
            task.title,
            task.category,
            f"[{color}]{days_text}[/{color}]",
            f"{status_emoji[task.status]} {task.status.value}",
            task.priority.value,
        )

    console.print(table)


@app.command("complete")
def complete_task(task_id: str = typer.Argument(..., help="ID da tarefa")):
    """Marca tarefa como concluída."""
    tasks = db.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)

    if not task:
        console.print(f"[red]Tarefa {task_id} não encontrada.[/red]")
        raise typer.Exit(1)

    task.complete()
    db.save_tasks(tasks)
    console.print(f"[green]✓[/green] Tarefa '{task.title}' concluída! 🎉")


@app.command("dashboard")
def show_dashboard():
    """
    Exibe dashboard completo com visão geral do progresso.
    """
    tasks = db.load_tasks()
    milestones = db.load_milestones()

    # Estatísticas
    total = len(tasks)
    completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
    in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
    overdue = len([t for t in tasks if t.is_overdue()])

    # Layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="stats", size=8),
        Layout(name="urgent", size=10),
        Layout(name="milestones", size=10),
    )

    # Header
    layout["header"].update(
        Panel(
            "[bold cyan]RSL Progress Tracker[/bold cyan] 📊",
            subtitle=f"Data: {date.today().strftime('%d/%m/%Y')}",
        )
    )

    # Stats
    stats_table = Table(show_header=False, box=box.SIMPLE)
    stats_table.add_column("Métrica", style="bold")
    stats_table.add_column("Valor", style="cyan")
    stats_table.add_row("Total de Tarefas", str(total))
    stats_table.add_row("Concluídas", f"[green]{completed}[/green]")
    stats_table.add_row("Em Progresso", f"[yellow]{in_progress}[/yellow]")
    stats_table.add_row("Atrasadas", f"[red]{overdue}[/red]")

    if total > 0:
        progress_pct = (completed / total) * 100
        stats_table.add_row("Progresso", f"{progress_pct:.1f}%")

    layout["stats"].update(Panel(stats_table, title="📈 Estatísticas"))

    # Tarefas urgentes (próximos 7 dias)
    urgent_tasks = [
        t
        for t in tasks
        if 0 <= t.days_remaining() <= 7 and t.status != TaskStatus.COMPLETED
    ]
    urgent_tasks = sorted(urgent_tasks, key=lambda t: t.deadline)[:5]

    if urgent_tasks:
        urgent_table = Table(box=box.SIMPLE)
        urgent_table.add_column("Tarefa", style="white")
        urgent_table.add_column("Prazo", style="yellow")

        for task in urgent_tasks:
            days_text, color = format_days_remaining(task.days_remaining())
            urgent_table.add_row(task.title, f"[{color}]{days_text}[/{color}]")

        layout["urgent"].update(Panel(urgent_table, title="⚠️  Tarefas Urgentes"))
    else:
        layout["urgent"].update(
            Panel(
                "[green]Nenhuma tarefa urgente![/green]", title="⚠️  Tarefas Urgentes"
            )
        )

    # Milestones
    if milestones:
        milestone_table = Table(box=box.SIMPLE)
        milestone_table.add_column("Marco", style="bold")
        milestone_table.add_column("Data Alvo", style="cyan")
        milestone_table.add_column("Tempo Restante", style="yellow")

        for milestone in sorted(milestones, key=lambda m: m.target_date)[:3]:
            days = milestone.days_until()
            days_text, color = format_days_remaining(days)
            status = "✅" if milestone.is_achieved else "🎯"

            milestone_table.add_row(
                f"{status} {milestone.title}",
                milestone.target_date.strftime("%d/%m/%Y"),
                f"[{color}]{days_text}[/{color}]",
            )

        layout["milestones"].update(
            Panel(milestone_table, title="🎯 Marcos Importantes")
        )

    console.print(layout)


@app.command("milestone-add")
def add_milestone(
    title: str = typer.Argument(..., help="Título do marco"),
    description: str = typer.Option("", "--desc", "-d", help="Descrição"),
    target_date: str = typer.Option(
        ..., "--date", "-dt", help="Data alvo (YYYY-MM-DD)"
    ),
):
    """Adiciona novo marco importante."""
    try:
        target = parse_date_input(target_date)
    except ValueError as e:
        console.print(f"[red]Erro: {e}[/red]")
        raise typer.Exit(1)

    milestone = Milestone(
        id=str(uuid.uuid4())[:8],
        title=title,
        description=description,
        target_date=target,
    )

    milestones = db.load_milestones()
    milestones.append(milestone)
    db.save_milestones(milestones)

    console.print(f"[green]✓[/green] Marco '{title}' adicionado!")
