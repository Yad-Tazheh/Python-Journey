from models.user import User
from models.task import Task
from models.project import Project
from storage.data_manager import DataManager


# test No1 - add user
def test_add_user():
    project = Project("Website", "p1")

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    project.add_user(user)

    assert len(project.users) == 1
    assert project.users[0].name == "Ali"

# test No2 - assign task
def test_assign_task():
    project = Project("Website", "p1")

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    task = Task(
        "Build API",
        "create backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    project.add_user(user)
    project.add_task(task)

    project.assign_task(
        task.task_id,
        user.user_id
    )

    assert task.assigned_user == user
    assert task in user.tasks


# test No3 - load and save in/from JSON file
def test_save_and_load(tmp_path):
    file = tmp_path / "project.json"

    manager = DataManager(file)

    project = Project("Website", "p1")

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    task = Task(
        "Build API",
        "create backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    project.add_user(user)
    project.add_task(task)

    project.assign_task(
        task.task_id,
        user.user_id
    )

    manager.save(project)

    loaded_project = manager.load()

    loaded_user = loaded_project.find_user(1)
    loaded_task = loaded_project.find_task(task.task_id)

    assert loaded_user.name == "Ali"
    assert loaded_task.title == "Build API"
    assert loaded_task.assigned_user == loaded_user
    assert loaded_task in loaded_user.tasks