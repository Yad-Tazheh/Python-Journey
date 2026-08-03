import sqlite3

from models.project import Project
from models.task import Task
from models.user import User


class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row # for returning select as a string not tuple
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_users(
                    project_id
                    TEXT,
                    user_id INTEGER,
                    PRIMARY KEY (project_id, user_id),
                    FOREIGN KEY (project_id)
                        REFERENCES projects(project_id),
                    FOREIGN KEY(user_id)
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
                task.project_id,
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
        if self.get_task(task_id) is None:
            raise ValueError("Task does not exist")

        if self.get_user(assigned_user_id) is None:
            raise ValueError("User does not exist")

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



    def delete_task(self, task_id):
        self.cursor.execute(
            """
            DELETE FROM tasks
            WHERE task_id = ?
            """,
            (task_id,)

        )

        if self.cursor.rowcount == 0:
            raise ValueError("Task does not exist")

        self.connection.commit()

    def delete_user(self, user_id):
        self.cursor.execute(
            """
            UPDATE tasks
            SET assigned_user_id = NULL
            WHERE assigned_user_id = ?""",
            (user_id,)
        )
        self.cursor.execute(
            """
            DELETE FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )
        if self.cursor.rowcount == 0:
            raise ValueError("User does not exist")

        self.connection.commit()

    def add_project(self, project):
        self.cursor.execute(
            """
            INSERT INTO projects
            (project_id, name)
            VALUES (?, ?)
            """,
            (project.project_id, project.name)
        )
        self.connection.commit()

    def get_project(self, project_id):
        self.cursor.execute(
            """
            SELECT * FROM projects 
            WHERE project_id = ?""",
            (project_id,)
        )
        row = self.cursor.fetchone()
        if row is None:
            return None

        return Project.from_row(row)

    def add_task_to_project(self, task_id, project_id):
        if self.get_task(task_id) is None:
            raise ValueError('task not found')

        if self.get_project(project_id) is None:
            raise ValueError('project not found')

        self.cursor.execute(
            """
            UPDATE tasks
            SET project_id = ?
            WHERE task_id = ?""",
            (project_id, task_id)
        )
        self.connection.commit()

    def get_project_tasks(self, project_id):
        self.cursor.execute(
            """
            SELECT * FROM tasks 
            WHERE project_id = ?""",
            (project_id,)
        )
        rows = self.cursor.fetchall()
        return [Task.from_row(row) for row in rows]

    def add_user_to_project(self, project_id, user_id):
        if self.get_user(user_id) is None:
            raise ValueError('user not found')

        if self.get_project(project_id) is None:
            raise ValueError('project not found')

        self.cursor.execute(
            """
            INSERT INTO project_users
                (project_id, user_id)
            VALUES (?, ?)
            """,
            (
                project_id,
                user_id
            )
        )


        self.connection.commit()

    def get_project_users(self, project_id):
        self.cursor.execute(
            """
            SELECT users.*
            FROM users
            JOIN project_users
            ON users.user_id = project_users.user_id
            WHERE project_users.project_id = ?
            """,
            (project_id,)
        )

        rows = self.cursor.fetchall()

        return [
            User.from_row(row)
            for row in rows
        ]
    def close(self):
        self.connection.close()