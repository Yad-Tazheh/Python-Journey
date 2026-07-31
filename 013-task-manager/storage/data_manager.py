import json

from models.project import Project

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