from enum import Enum

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

    @classmethod
    def from_row(cls, row):
        user = cls(
            row["name"],
            row["user_id"],
            row["email"]
        )
        user.role = cls.Roles(row["role"])
        return user
