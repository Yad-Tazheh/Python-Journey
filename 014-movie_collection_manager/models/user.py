from database.database import Base

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    # a reviews belong to "a" user not reviews belong to users
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user",
    )