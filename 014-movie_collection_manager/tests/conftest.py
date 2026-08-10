from dotenv import load_dotenv

load_dotenv(".env.test")

from database.base import Base
from database.database import engine
import pytest
from database.database import SessionLocal

# these are imported so alchemy can find the foreign keys associated to each models example actor_id
from models.actor import Actor
from models.genre import Genre
from models.movie import Movie
from models.review import Review
from models.user import User


@pytest.fixture
def test_session():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)