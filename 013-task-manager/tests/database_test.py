from database.db_manager import DatabaseManager
from models.project import Project
from models.user import User
from models.task import Task


def test_save_and_get_user(tmp_path):
    db_file = tmp_path / "test.db"

    db = DatabaseManager(db_file)

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    db.add_user(user)

    result = db.get_user(1)

    assert result.name == "Ali"


def test_save_and_get_task(tmp_path):
    db_file = tmp_path / "test.db"

    db = DatabaseManager(db_file)

    task = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    db.add_task(task)

    result = db.get_task(task.task_id)

    assert result.title == "Build API"

def test_update_task_status(tmp_path):
    db_file = tmp_path / "test.db"

    db = DatabaseManager(db_file)

    task = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    db.add_task(task)

    db.update_task_status(
        task.task_id,
        Task.Status.DONE
    )

    updated_task = db.get_task(task.task_id)

    assert updated_task.status == Task.Status.DONE
def test_assign_task(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseManager(db_file)

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )
    task = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    db.add_user(user)
    db.add_task(task)

    db.assign_task(task.task_id, user.user_id)
    loaded_task = db.get_task(task.task_id)

    assert loaded_task.title == "Build API"


def test_get_user_tasks(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseManager(db_file)

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    task1 = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    task2 = Task(
        "Design Login",
        "frontend",
        Task.Priority.MEDIUM,
        "2026-08-02"
    )
    db.add_user(user)
    db.add_task(task1)
    db.add_task(task2)

    db.assign_task(task1.task_id, user.user_id)
    db.assign_task(task2.task_id, user.user_id)

    loaded_tasks = db.get_user_tasks(user.user_id)

    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Build API"
    assert loaded_tasks[1].title == "Design Login"

def test_delete_task(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseManager(db_file)

    task = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )
    db.add_task(task)
    db.delete_task(task.task_id)
    result = db.get_task(task.task_id)
    assert result is None

def test_delete_user(tmp_path):
    db_file = tmp_path / "test.db"

    db = DatabaseManager(db_file)

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    task = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    db.add_user(user)
    db.add_task(task)

    db.assign_task(
        task.task_id,
        user.user_id
    )

    db.delete_user(user.user_id)

    deleted_user = db.get_user(user.user_id)
    remaining_task = db.get_task(task.task_id)

    assert deleted_user is None
    assert remaining_task.assigned_user_id is None

def test_save_and_get_project(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseManager(db_file)

    project = Project(
        "Website",
        "p1"
    )
    db.add_project(project)
    result = db.get_project("p1")
    assert result.name == "Website"

def test_add_task_to_project(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseManager(db_file)

    project = Project(
        "Website",
        "p1"
    )

    task = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )
    db.add_project(project)
    db.add_task(task)
    db.add_task_to_project(task.task_id, project.project_id)

    loaded_task = db.get_task(task.task_id)
    assert loaded_task.project_id == "p1"
def test_get_project_tasks(tmp_path):
    db_file = tmp_path / "test.db"

    db = DatabaseManager(db_file)

    project = Project(
        "Website",
        "p1"
    )

    task1 = Task(
        "Build API",
        "backend",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    task2 = Task(
        "Design Login",
        "frontend",
        Task.Priority.MEDIUM,
        "2026-08-02"
    )

    db.add_project(project)

    db.add_task(task1)
    db.add_task(task2)

    db.add_task_to_project(
        task1.task_id,
        project.project_id
    )

    db.add_task_to_project(
        task2.task_id,
        project.project_id
    )

    tasks = db.get_project_tasks(project.project_id)

    assert len(tasks) == 2
    assert tasks[0].title == "Build API"
    assert tasks[1].title == "Design Login"

def test_add_user_to_project(tmp_path):
    db_file = tmp_path / "test.db"

    db = DatabaseManager(db_file)

    project = Project(
        "Website",
        "p1"
    )

    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

    db.add_project(project)
    db.add_user(user)

    db.add_user_to_project(project.project_id,user.user_id)

    users = db.get_project_users(project.project_id)

    assert len(users) == 1
    assert users[0].name == "Ali"