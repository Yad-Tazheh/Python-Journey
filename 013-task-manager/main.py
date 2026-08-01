from models.project import Project
from models.user import User
from models.task import Task
from storage.data_manager import DataManager
from database.db_manager import DatabaseManager

from models.user import User
from models.task import Task
from models.project import Project
from storage.data_manager import DataManager


def main():
    db = DatabaseManager('project.db')
    db.create_tables()
    user = User(
        "Ali",
        1,
        "ali@test.com"
    )

#    db.add_user(user)
    db.get_user(1)
    task = Task(
        "Docker",
        "Build Docker container",
        Task.Priority.HIGH,
        "2026-08-01"
    )

    db.add_task(task)
    print(db.get_task(task.task_id))

    loaded_task = db.get_task(task.task_id)
    print(loaded_task)

    db.close()


###########################################################
#    manager = DataManager("project.json")
#
#    # make a project
#    project = Project("Website", "p1")
#
#    # generate user
#    user = User(
#        "Ali",
#        1,
#        "ali@test.com"
#    )
#
#    # generate task
#    task = Task(
#        "Build API",
#        "Create backend API",
#        Task.Priority.HIGH,
#        "2026-08-01"
#    )
#
#    # add
#    project.add_user(user)
#    project.add_task(task)
#
#    # Assign
#    project.assign_task(task.task_id, user.user_id)
#
#    # save
#    manager.save(project)
#
#    # load
#    loaded_project = manager.load()
#
#    # show
#    print(loaded_project.name)
#    loaded_project.show_users()
#    loaded_project.show_tasks()
#


if __name__ == "__main__":
    main()