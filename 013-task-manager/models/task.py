from enum import Enum
from uuid import uuid7
from datetime import datetime

class Task:
    class Status(Enum):
        PENDING = 'pending'
        TODO = 'todo'
        IN_PROGRESS = 'in_progress'
        DONE = 'done'
        CANCELED = 'canceled'

    class Priority(Enum):
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'

    def __init__(self, title, description,priority, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.created_at = datetime.now()
        self.task_id = str(uuid7())

        self.assigned_user = None
        self.assigned_user_id= None
        self.project_id = None

        self.status = Task.Status.TODO
        if not isinstance(priority, Task.Priority):
            raise TypeError("Priority must be of type Task.Priority")
        self.priority = priority

    def __str__(self):
        assigned = self.assigned_user.name if self.assigned_user else "Unassigned"
        return (
            f"task: {self.title}, "
            f"assigned to: {assigned}, "
            f"priority: {self.priority.value}, "
            f"created_at: {self.created_at}, "
            f"due_date: {self.due_date}, "
            f"status: {self.status.value}, "

        )

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date,
            "assigned_user": (
                self.assigned_user.user_id
                if self.assigned_user
                else None
            )
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            data["title"],
            data["description"],
            Task.Priority(data["priority"]),
            data["due_date"]
        )

        task.task_id = data["task_id"]
        task.status = Task.Status(data["status"])
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.project_id = data["project_id"]

        return task

    @classmethod
    def from_row(cls, row):
        task = cls(
            row["title"],
            row["description"],
            Task.Priority(row["priority"]),
            row["due_date"]
        )
        task.task_id = row["task_id"]
        task.status = cls.Status(row["status"])
        task.assigned_user_id = row["assigned_user_id"]
        task.created_at = datetime.fromisoformat(row["created_at"])
        task.project_id = row["project_id"]
        return task