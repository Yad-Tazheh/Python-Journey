from database.database import Base

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.association import movie_actors


class Actor(Base):
    __tablename__ = "actors"


    actor_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movie_actors",
        back_populates="actors",
    )

