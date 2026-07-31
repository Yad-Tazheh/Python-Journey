import json
from enum import Enum
from uuid import uuid7
from datetime import datetime


class User:

    class Roles(Enum):
        ADMIN = 'admin'
        USER = 'user'
        MANAGER = 'manager'

    def __init__(self, name, user_id, email):
        self.name = name
        self.user_id = user_id # usually its ssn so better not use uuid
        self.email = email
        self.role = User.Roles.USER
        self.tasks = []

    def __str__(self):
        return f'{self.name} | {self.user_id} | {self.email} | {self.role.value}'

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "email": self.email,
            "role": self.role.value,
            "tasks": [task.task_id for task in self.tasks]
        }

    # method belongs to the class itself not a created object
    # means run the function on the class itself not the instances of the class
    @classmethod
    def from_dict(cls, data):
        # import User.__init__ args from the json field data
        user = cls(
            data["name"],
            data["user_id"],
            data["email"]
        )
        # import the role as well
        user.role = User.Roles(data["role"])
        return user

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

        return task


class Project:
    def __init__(self, name, project_id):
        self.name = name
        self.project_id = project_id
        self.tasks = []
        self.users = []

    def to_dict(self):
        return {
            "name": self.name,
            "project_id": self.project_id,
            "tasks": [task.to_dict() for task in self.tasks],
            "users": [user.to_dict() for user in self.users]
        }
    @classmethod
    def from_dict(cls, data):
        project = cls(
            data["name"],
            data["project_id"]
        )
        for user_data in data["users"]:
            user = User.from_dict(user_data)
            project.add_user(user)

        for task_data in data["tasks"]:
            task = Task.from_dict(task_data)
            project.add_task(task)

        for task_data in data["tasks"]:
            assigned_user_id = task_data["assigned_user"]

            if assigned_user_id:
                task = project.find_task(task_data["task_id"])
                user = project.find_user(assigned_user_id)

                if task and user:
                    task.assigned_user = user
                    user.tasks.append(task)

        return project


    def add_user(self, user):
        if user is None:
            raise ValueError("User cannot be None")
        if user in self.users:
            raise ValueError("User already exists")
        self.users.append(user)
        return user

    def add_task(self, task):
        if task is None:
            raise ValueError("Task cannot be None")
        if task in self.tasks:
            raise ValueError("Task already exists")
        self.tasks.append(task)
        return task

    def find_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def find_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    # find and check user and the task both exists
    # if task assigned to a user then remove task from previous user's tasks list
    # assign the new user to the task
    # assign task to the new user's tasks list (if it's not alr there)
    # return the task
    def assign_task(self, task_id, user_id):
        task = self.find_task(task_id)
        if task is None:
            raise ValueError("Task does not exist")

        user = self.find_user(user_id)
        if user is None:
            raise ValueError("User does not exist")

        if task.assigned_user is not None:
            task.assigned_user.tasks.remove(task)
        task.assigned_user = user

        if task not in user.tasks:
            user.tasks.append(task)
        return task

    # find and check the task exists
    # if task is assigned to a user then remove the task from the user's tasks list
    # remove the task from the project's tasks list
    # return task
    def remove_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            raise ValueError("Task does not exist")

        if task.assigned_user is not None:
            task.assigned_user.tasks.remove(task)

        self.tasks.remove(task)
        return task

    # find and check if the user exists
    # for each task assigned to the user
    # unassign the task
    # clear the user's task list
    # remove the user from the project's users list
    # return the user
    def remove_user(self, user_id):
        user = self.find_user(user_id)
        if user is None:
            raise ValueError("User does not exist")

        for task in user.tasks[:]:
            task.assigned_user = None

        user.tasks.clear()
        self.users.remove(user)
        return user

    # find and check if the task exists
    # validate the new status
    # change the task.status value into the given value
    # return the task
    def change_task_status(self, task_id, status):
        task = self.find_task(task_id)
        if task is None:
            raise ValueError("Task does not exist")
        if not isinstance(status, Task.Status):
            raise TypeError("Status must be of type Task.Status")
        task.status = status
        return task

    # for each task in project's tasks list
    # print the task.__str__
    def show_tasks(self):
        for task in self.tasks:
            print(task)

    def show_users(self):
        for user in self.users:
            print(user)

    # find and check if the user exists
    # loop through users tasks
    # show each task
    def show_users_tasks(self, user_id):
        user = self.find_user(user_id)
        if user is None:
            raise ValueError("User does not exist")
        for task in user.tasks:
            print(task)

    def change_user_role(self, user_id, role):
        user = self.find_user(user_id)
        if user is None:
            raise ValueError("User does not exist")
        if not isinstance(role, User.Roles):
            raise TypeError("Role must be of type User.Roles")
        user.role = role
        return user


    # show project name
    # show how many users working on the proj
    # show how many tasks the project have
    # show how many tasks are done
    # show how many tasks are in pending mode
    def project_summary(self):
        done_tasks = sum(
            1 for task in self.tasks
            if task.status == Task.Status.DONE
        )
        pending_tasks = sum(
            1 for task in self.tasks
            if task.status == Task.Status.PENDING
        )

        return (
            f'project: {self.name}, '
            f'users: {len(self.users)}, '
            f'tasks: {len(self.tasks)}, '
            f'done: {done_tasks}, '
            f'pending: {pending_tasks}'
        )

class DataManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def save(self, project):
        with open(self.file_name, "w") as file:
            json.dump(project.to_dict(), file, indent=4)

    def load(self):
        with open(self.file_name, "r") as file:
            data = json.load(file)

        return Project.from_dict(data)

if __name__ == "__main__":
    manager = DataManager("project.json")
    #
    #project = Project("Website", "p1")
    #
    #user = User("Ali", 1, "ali@test.com")
    #task = Task(
    #    "Build API",
    #    "create backend",
    #    Task.Priority.HIGH,
    #    "2026-08-01"
    #)
    #
    #project.add_user(user)
    #project.add_task(task)
    #
    #project.assign_task(task.task_id, user.user_id)
    #
    #manager.save(project)
    loaded_project = manager.load()

    loaded_project.show_tasks()