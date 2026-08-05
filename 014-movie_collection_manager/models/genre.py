from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Genre(Base):
    __tablename__ = "genres"

    genre_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name : Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
