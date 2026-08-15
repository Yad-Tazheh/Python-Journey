from dotenv import load_dotenv

# Load test environment before importing the database engine.
load_dotenv(".env.test", override=True)

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from database.base import Base
from database.database import engine, SessionLocal
from dependencies import get_session
from main import app

# Models
from models.actor import Actor
from models.genre import Genre
from models.movie import Movie
from models.review import Review
from models.user import User

# Repositories
from repositories.actor_repository import ActorRepository
from repositories.genre_repository import GenreRepository
from repositories.movie_repository import MovieRepository
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository

# Services
from services.actor_service import ActorService
from services.genre_serive import GenreService
from services.movie_service import MovieService
from services.review_service import ReviewService
from services.user_service import UserService


@pytest.fixture
def test_session() -> Session:
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# ------------------------------------------------------------------
# Service fixtures
# ------------------------------------------------------------------


@pytest.fixture
def movie_service(test_session: Session) -> MovieService:
    movie_repository = MovieRepository(test_session)
    actor_repository = ActorRepository(test_session)
    genre_repository = GenreRepository(test_session)

    return MovieService(
        movie_repository=movie_repository,
        actor_repository=actor_repository,
        genre_repository=genre_repository,
    )


@pytest.fixture
def actor_service(test_session: Session) -> ActorService:
    actor_repository = ActorRepository(test_session)
    movie_repository = MovieRepository(test_session)

    return ActorService(
        actor_repository=actor_repository,
        movie_repository=movie_repository,
    )


@pytest.fixture
def genre_service(test_session: Session) -> GenreService:
    genre_repository = GenreRepository(test_session)
    movie_repository = MovieRepository(test_session)

    return GenreService(
        genre_repository=genre_repository,
        movie_repository=movie_repository,
    )


@pytest.fixture
def user_service(test_session: Session) -> UserService:
    user_repository = UserRepository(test_session)

    return UserService(
        user_repository=user_repository,
    )


@pytest.fixture
def review_service(test_session: Session) -> ReviewService:
    review_repository = ReviewRepository(test_session)
    user_repository = UserRepository(test_session)
    movie_repository = MovieRepository(test_session)

    return ReviewService(
        review_repository=review_repository,
        user_repository=user_repository,
        movie_repository=movie_repository,
    )


# ------------------------------------------------------------------
# FastAPI client
# ------------------------------------------------------------------


@pytest.fixture
def client(test_session: Session):
    def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# ------------------------------------------------------------------
# Common test data
# ------------------------------------------------------------------


@pytest.fixture
def test_user(test_session: Session) -> User:
    user = User(username="Test")

    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)

    return user


@pytest.fixture
def test_movie(test_session: Session) -> Movie:
    movie = Movie(
        title="Test Movie",
        description="A test movie",
        release_date="2023-01-01",
    )

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    return movie