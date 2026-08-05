from enum import Enum
from sqlalchemy import Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import  Base
from models.association import project_users

class Roles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    MANAGER = "MANAGER"

class User(Base):
    """Represents a user in the task manager."""
    __tablename__ = "users"
    user_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, nullable=False)
    role : Mapped[Roles] = mapped_column(SQLEnum(Roles), nullable=False, default=Roles.USER)
    tasks : Mapped[list["Task"]] = relationship(back_populates="assigned_user") # type hint of list[]
    projects: Mapped[list["Project"]] = relationship(secondary=project_users,back_populates="users")

