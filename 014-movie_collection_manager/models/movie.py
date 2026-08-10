from database.database import Base

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

# this has to be imported cause both movies and genres needs to see the many-to-many relationship
from models.association import movie_genres, movie_actors


class Movie(Base):
    __tablename__ = "movies"


    movie_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    release_date: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # forward referencing to Genre class
    genres: Mapped[list["Genre"]] = relationship(
        secondary="movie_genres",
        back_populates="movies",
    )

    actors: Mapped[list["Actor"]] = relationship(
        secondary="movie_actors",
        back_populates="movies",
    )

    # cascade relates operations on movies to reviews
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
    )