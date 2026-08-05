from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from models.association import project_users

class Project(Base):
    __tablename__ = "projects"

    project_id : Mapped[str] = mapped_column(String, primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    tasks : Mapped[list["Task"]] = relationship(back_populates="project")
    users : Mapped[list["User"]] = relationship(secondary=project_users, back_populates="projects")

