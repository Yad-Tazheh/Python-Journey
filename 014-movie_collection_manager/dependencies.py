from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from repositories.actor_repository import ActorRepository
from repositories.genre_repository import GenreRepository
from repositories.movie_repository import MovieRepository
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository
from services.actor_service import ActorService
from services.genre_serive import GenreService
from services.movie_service import MovieService
from services.review_service import ReviewService
from services.user_service import UserService


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_movie_service(
    db: Session = Depends(get_session),
):
    movie_repository = MovieRepository(db)
    actor_repository = ActorRepository(db)
    genre_repository = GenreRepository(db)

    return MovieService(
        movie_repository=movie_repository,
        actor_repository=actor_repository,
        genre_repository=genre_repository,
    )


def get_actor_service(
    db: Session = Depends(get_session),
):
    actor_repository = ActorRepository(db)
    movie_repository = MovieRepository(db)

    return ActorService(
        actor_repository=actor_repository,
        movie_repository=movie_repository,
    )


def get_genre_service(
    db: Session = Depends(get_session),
):
    genre_repository = GenreRepository(db)
    movie_repository = MovieRepository(db)

    return GenreService(
        genre_repository=genre_repository,
        movie_repository=movie_repository,
    )


def get_user_service(
    db: Session = Depends(get_session),
):
    repository = UserRepository(db)

    return UserService(repository)


def get_review_service(
    db: Session = Depends(get_session),
):
    review_repository = ReviewRepository(db)
    movie_repository = MovieRepository(db)
    user_repository = UserRepository(db)

    return ReviewService(
        review_repository=review_repository,
        user_repository=user_repository,
        movie_repository=movie_repository,
    )