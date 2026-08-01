from database.db_manager import DatabaseManager
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