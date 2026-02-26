"""
Gerenciamento de persistência de dados em SQLite.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from phd_progress_tracker.models.task import Task, TaskPriority, TaskStatus
from phd_progress_tracker.models.milestone import Milestone


class Database:
    """Gerencia persistência de tarefas e milestones em SQLite."""

    # Constant for in-memory database path
    IN_MEMORY_PATH = ":memory:"

    def __init__(self, data_dir: str = "data", db_path: Optional[str] = None):
        """
        Inicializa database SQLite.

        Args:
            data_dir: Diretório onde dados serão salvos
            db_path: Caminho alternativo para o banco SQLite (para testes)
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # JSON files (legacy, for migration)
        self.tasks_file = self.data_dir / "tasks.json"
        self.milestones_file = self.data_dir / "milestones.json"

        # SQLite database
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = self.data_dir / "phd_tracker.db"

        # For in-memory databases, keep a single connection
        self._connection: Optional[sqlite3.Connection] = None
        self._is_memory = str(self.db_path) == self.IN_MEMORY_PATH

        self._init_db()
        self._migrate_from_json()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna conexão com o banco de dados."""
        if self._is_memory:
            if self._connection is None:
                self._connection = sqlite3.connect(
                    str(self.db_path), check_same_thread=False
                )
                self._connection.row_factory = sqlite3.Row
            return self._connection
        else:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            return conn

    def close(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> "Database":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def _init_db(self) -> None:
        """Cria as tabelas se não existirem."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        deadline TEXT NOT NULL,
                        status TEXT NOT NULL,
                        priority TEXT NOT NULL,
                        category TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        completed_at TEXT
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS milestones (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        target_date TEXT NOT NULL,
                        is_achieved INTEGER NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to initialize database: {e}") from e

    def _data_exists_in_db(self) -> bool:
        """Verifica se já existem dados no banco SQLite."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM tasks")
                tasks_count = cursor.fetchone()[0]
                cursor = conn.execute("SELECT COUNT(*) FROM milestones")
                milestones_count = cursor.fetchone()[0]
                return tasks_count > 0 or milestones_count > 0
        except sqlite3.Error:
            # If tables don't exist or other error, assume no data
            return False

    def _migrate_from_json(self) -> None:
        """Migra dados de JSON para SQLite se existirem arquivos JSON."""
        # Check if migration already happened (idempotency)
        if self._data_exists_in_db():
            return

        # Check if JSON files exist
        if not self.tasks_file.exists() and not self.milestones_file.exists():
            return

        try:
            with self._get_connection() as conn:
                # Begin transaction for atomic migration
                conn.execute("BEGIN TRANSACTION")

                try:
                    # Migrate tasks
                    if self.tasks_file.exists():
                        with open(self.tasks_file, "r", encoding="utf-8") as f:
                            tasks_data = json.load(f)

                        for task_data in tasks_data:
                            conn.execute(
                                """
                                INSERT OR REPLACE INTO tasks
                                (id, title, description, deadline, status, priority, category, created_at, completed_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                                (
                                    task_data["id"],
                                    task_data["title"],
                                    task_data["description"],
                                    task_data["deadline"],
                                    task_data["status"],
                                    task_data["priority"],
                                    task_data["category"],
                                    task_data["created_at"],
                                    task_data.get("completed_at"),
                                ),
                            )

                        # Backup and remove JSON file
                        backup_dir = self.data_dir / "json_backup"
                        backup_dir.mkdir(exist_ok=True)
                        self.tasks_file.rename(backup_dir / "tasks.json")

                    # Migrate milestones
                    if self.milestones_file.exists():
                        with open(self.milestones_file, "r", encoding="utf-8") as f:
                            milestones_data = json.load(f)

                        for m_data in milestones_data:
                            conn.execute(
                                """
                                INSERT OR REPLACE INTO milestones
                                (id, title, description, target_date, is_achieved)
                                VALUES (?, ?, ?, ?, ?)
                            """,
                                (
                                    m_data["id"],
                                    m_data["title"],
                                    m_data["description"],
                                    m_data["target_date"],
                                    1 if m_data["is_achieved"] else 0,
                                ),
                            )

                        # Backup and remove JSON file
                        backup_dir = self.data_dir / "json_backup"
                        backup_dir.mkdir(exist_ok=True)
                        self.milestones_file.rename(backup_dir / "milestones.json")

                    conn.commit()

                except Exception as e:
                    conn.rollback()
                    raise RuntimeError(f"Migration failed: {e}") from e

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error during migration: {e}") from e

    def save_tasks(self, tasks: List[Task]) -> None:
        """Salva lista de tarefas no SQLite."""
        try:
            with self._get_connection() as conn:
                # Clear existing tasks
                conn.execute("DELETE FROM tasks")

                # Insert all tasks
                for task in tasks:
                    conn.execute(
                        """
                        INSERT INTO tasks
                        (id, title, description, deadline, status, priority, category, created_at, completed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            task.id,
                            task.title,
                            task.description,
                            task.deadline.isoformat(),
                            task.status.name,
                            task.priority.name,
                            task.category,
                            task.created_at.isoformat(),
                            (
                                task.completed_at.isoformat()
                                if task.completed_at
                                else None
                            ),
                        ),
                    )
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to save tasks: {e}") from e

    def load_tasks(self) -> List[Task]:
        """Carrega lista de tarefas do SQLite."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, title, description, deadline, status, priority, category, created_at, completed_at
                    FROM tasks
                """)
                rows = cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to load tasks: {e}") from e

        tasks = []
        for row in rows:
            tasks.append(
                Task(
                    id=row["id"],
                    title=row["title"],
                    description=row["description"],
                    deadline=datetime.fromisoformat(row["deadline"]).date(),
                    status=TaskStatus[row["status"]],
                    priority=TaskPriority[row["priority"]],
                    category=row["category"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    completed_at=(
                        datetime.fromisoformat(row["completed_at"])
                        if row["completed_at"]
                        else None
                    ),
                )
            )
        return tasks

    def save_milestones(self, milestones: List[Milestone]) -> None:
        """Salva lista de milestones no SQLite."""
        try:
            with self._get_connection() as conn:
                # Clear existing milestones
                conn.execute("DELETE FROM milestones")

                # Insert all milestones
                for milestone in milestones:
                    conn.execute(
                        """
                        INSERT INTO milestones
                        (id, title, description, target_date, is_achieved)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            milestone.id,
                            milestone.title,
                            milestone.description,
                            milestone.target_date.isoformat(),
                            1 if milestone.is_achieved else 0,
                        ),
                    )
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to save milestones: {e}") from e

    def load_milestones(self) -> List[Milestone]:
        """Carrega lista de milestones do SQLite."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, title, description, target_date, is_achieved
                    FROM milestones
                """)
                rows = cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to load milestones: {e}") from e

        milestones = []
        for row in rows:
            milestones.append(
                Milestone(
                    id=row["id"],
                    title=row["title"],
                    description=row["description"],
                    target_date=datetime.fromisoformat(row["target_date"]).date(),
                    is_achieved=bool(row["is_achieved"]),
                )
            )
        return milestones
