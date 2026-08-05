from models.user import User, Roles
from models.task import Task, TaskPriority, TaskStatus
from models.project import Project


def test_create_user(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    test_session.add(user)

    test_session.commit()

    result = test_session.get(User, 1)

    assert result.name == "Ali"
    assert result.email == "ali@test.com"
    assert result.role == Roles.ADMIN

def test_create_user(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    test_session.add(user)
    test_session.commit()

    result = test_session.get(User, 1)

    assert result is not None
    assert result.name == "Ali"
    assert result.email == "ali@test.com"
    assert result.role == Roles.ADMIN



def test_get_user(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    test_session.add(user)
    test_session.commit()

    result = test_session.get(User, 1)

    assert result is not None
    assert result.user_id == 1
    assert result.name == "Ali"
    assert result.email == "ali@test.com"
    assert result.role == Roles.ADMIN


def test_update_user_role(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.USER
    )

    test_session.add(user)
    test_session.commit()

    user.role = Roles.MANAGER

    test_session.commit()

    updated_user = test_session.get(User, 1)

    assert updated_user.role == Roles.MANAGER


def test_delete_user(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    test_session.add(user)
    test_session.commit()

    test_session.delete(user)

    test_session.commit()

    deleted_user = test_session.get(User, 1)

    assert deleted_user is None


def test_create_task(test_session):
    task = Task(
        task_id = "task-1",
        title = "Build API",
        description="Backend API",
        priority=TaskPriority.HIGH,
        due_date="2026-08-10"

    )
    test_session.add(task)
    test_session.commit()

    loaded_task = test_session.get(Task, "task-1")

    assert loaded_task is not None
    assert loaded_task.title == "Build API"
    assert loaded_task.description == "Backend API"
    assert loaded_task.priority == TaskPriority.HIGH
    assert loaded_task.status == TaskStatus.TODO


def test_update_task_status(test_session):
    task = Task(
        task_id="task-1",
        title="Build API",
        description="Backend API",
        priority=TaskPriority.HIGH,
        due_date="2026-08-10"
    )

    test_session.add(task)
    test_session.commit()

    task.status = TaskStatus.IN_PROGRESS
    test_session.commit()

    updated_task = test_session.get(Task, "task-1")

    assert updated_task.status == TaskStatus.IN_PROGRESS

def test_delete_task(test_session):
    task = Task(
        task_id="task-1",
        title="Build API",
        description="Backend API",
        priority=TaskPriority.HIGH,
        due_date="2026-08-10"
    )

    test_session.add(task)
    test_session.commit()

    test_session.delete(task)
    test_session.commit()

    deleted_task = test_session.get(Task, "task-1")

    assert deleted_task is None


def test_assign_task_to_user(test_session):
    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    task = Task(
        task_id="task-1",
        title="Build API",
        description="Backend API",
        priority=TaskPriority.HIGH
    )

    user.tasks.append(task)

    test_session.add(user)
    test_session.commit()
    loaded_user = test_session.get(User, 1)

    assert len(loaded_user.tasks) == 1
    assert loaded_user.tasks[0].title == "Build API"

def test_user_task_relationship(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    task = Task(
        task_id="task-1",
        title="Build API",
        description="Create backend API",
        priority=TaskPriority.HIGH
    )

    user.tasks.append(task)

    test_session.add(user)
    test_session.commit()

    loaded_user = test_session.get(User, 1)

    assert len(loaded_user.tasks) == 1
    assert loaded_user.tasks[0].title == "Build API"

    loaded_task = test_session.get(Task, "task-1")

    assert loaded_task.assigned_user.name == "Ali"

def test_create_project(test_session):
    project = Project(
        project_id="p1",
        name="Task Manager"
    )

    test_session.add(project)
    test_session.commit()

    loaded_project = test_session.get(
        Project,
        "p1"
    )

    assert loaded_project is not None
    assert loaded_project.name == "Task Manager"



def test_project_task_relationship(test_session):

    project = Project(
        project_id="p1",
        name="Task Manager"
    )

    task = Task(
        task_id="task-1",
        title="Create Database",
        description="Setup PostgreSQL",
        priority=TaskPriority.HIGH
    )

    project.tasks.append(task)

    test_session.add(project)
    test_session.commit()

    loaded_project = test_session.get(
        Project,
        "p1"
    )

    assert len(loaded_project.tasks) == 1
    assert loaded_project.tasks[0].title == "Create Database"

    loaded_task = test_session.get(
        Task,
        "task-1"
    )

    assert loaded_task.project.name == "Task Manager"


def test_project_task_relationship(test_session):

    project = Project(
        project_id="p1",
        name="Task Manager"
    )

    task = Task(
        task_id="task-1",
        title="Create Database",
        description="Setup PostgreSQL",
        priority=TaskPriority.HIGH
    )

    project.tasks.append(task)

    test_session.add(project)
    test_session.commit()

    loaded_project = test_session.get(Project, "p1")

    assert loaded_project is not None
    assert len(loaded_project.tasks) == 1
    assert loaded_project.tasks[0].title == "Create Database"

    loaded_task = test_session.get(Task, "task-1")

    assert loaded_task.project.name == "Task Manager"

def test_add_user_to_project(test_session):

    user = User(
        user_id=1,
        name="Ali",
        email="ali@test.com",
        role=Roles.ADMIN
    )

    project = Project(
        project_id="p1",
        name="Task Manager"
    )

    project.users.append(user)

    test_session.add(project)
    test_session.commit()

    loaded_project = test_session.get(Project, "p1")

    assert len(loaded_project.users) == 1
    assert loaded_project.users[0].name == "Ali"

    loaded_user = test_session.get(User, 1)

    assert len(loaded_user.projects) == 1
    assert loaded_user.projects[0].name == "Task Manager"