from enum import Enum
from datetime import datetime


from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import Base


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELED = "CANCELED"

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Task(Base):
    __tablename__ = "tasks"

    task_id : Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    title : Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    description : Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    status : Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO,
        nullable = False
    )
    priority : Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority),
        nullable=False
    )
    created_at : Mapped[datetime] = mapped_column(
        DateTime,
        default = datetime.utcnow
    )
    due_date : Mapped[str | None] = mapped_column(
        String,
        nullable = True
    )
    assigned_user_id : Mapped[int | None] = mapped_column(
        ForeignKey("users.user_id"),
        nullable = True
    )
    assigned_user : Mapped["User"] = relationship(
        back_populates = "tasks"
    )
    project_id : Mapped[str | None] = mapped_column(
        ForeignKey("projects.project_id"),
        nullable = True
    )
    project : Mapped["Project"] = relationship(
        back_populates="tasks"
    )



