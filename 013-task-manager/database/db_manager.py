import sqlite3

from models.task import Task
from models.user import User


class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL,
            due_date TEXT,
            project_id TEXT,
            assigned_user_id INTEGER,

            FOREIGN KEY(project_id)
                REFERENCES projects(project_id),

            FOREIGN KEY(assigned_user_id)
                REFERENCES users(user_id)
        )
        """)

        self.connection.commit()

    def add_user(self, user):
        existing = self.get_user(user.user_id)
        if existing:
            raise ValueError('user already exists')

        self.cursor.execute(
            """
            INSERT INTO users
                (user_id, name, email, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                user.user_id,
                user.name,
                user.email,
                user.role.value
            )
        )

        self.connection.commit()

    def add_task(self, task):
        self.cursor.execute(
            """
            INSERT INTO tasks
            (task_id, title, description, status, priority, created_at, due_date, project_id, assigned_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.task_id,
                task.title,
                task.description,
                task.status.value,
                task.priority.value,
                task.created_at.isoformat(),
                task.due_date,
                None,
                task.assigned_user.user_id if task.assigned_user else None,

             )
        )
        self.connection.commit()

    def get_user(self, user_id):
        self.cursor.execute(
            """
            SELECT * FROM users 
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return User.from_row(row)

    def get_task(self, task_id):
        self.cursor.execute(
            """
            SELECT * FROM tasks 
            WHERE task_id = ?""",
            (task_id,)

        )
        row = self.cursor.fetchone()
        if row is None:
            return None
        return Task.from_row(row)

    def update_task_status(self, task_id, status):
        self.cursor.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE task_id = ?
            """,
            (status.value, task_id)

        )
        self.connection.commit()

    # check if user exists
    # check if task exists
    # update assigned_user_id in tasks table
    def assign_task(self, task_id, assigned_user_id):
        self.cursor.execute(
            """
            UPDATE tasks
            SET assigned_user_id = ?
            WHERE task_id = ?
            """,
            (assigned_user_id, task_id)
        )
        self.connection.commit()

    def get_user_tasks(self, user_id):
        self.cursor.execute(
            """
            SELECT * FROM tasks 
            WHERE assigned_user_id = ?
            """,
            (user_id,)
        )
        rows = self.cursor.fetchall()

        return [Task.from_row(row) for row in rows]






    def close(self):
        self.connection.close()