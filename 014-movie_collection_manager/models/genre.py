from database.database import Base

from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped

from models.association import movie_genres


class Genre(Base):
    __tablename__ = "genres"


    genre_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movie_genres",
        back_populates="genres",
    )


    