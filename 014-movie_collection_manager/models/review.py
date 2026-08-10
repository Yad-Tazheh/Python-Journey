from database.database import Base

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Review(Base):
    __tablename__ = 'reviews'

    review_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
    )

    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("movies.movie_id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="reviews",
    )

    movie: Mapped["Movie"] = relationship(
        back_populates="reviews",
    )



