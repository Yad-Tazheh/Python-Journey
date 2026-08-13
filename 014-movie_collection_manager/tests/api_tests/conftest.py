from dotenv import load_dotenv

load_dotenv(".env.test")

import pytest
from fastapi.testclient import TestClient

from database.base import Base
from database.database import engine, SessionLocal

# Import models so SQLAlchemy knows all tables and relationships
from models.actor import Actor
from models.genre import Genre
from models.movie import Movie
from models.review import Review
from models.user import User

from main import app
from dependencies import get_session


@pytest.fixture
def test_session():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_session):
    def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_session):
    user = User(username="Test")

    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)

    return user


@pytest.fixture
def test_movie(test_session):
    movie = Movie(title="Test Movie", description="A test movie", release_date="2023-01-01")

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    return movie
