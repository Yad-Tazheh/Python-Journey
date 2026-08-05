from dotenv import load_dotenv

load_dotenv(".env.test")

from database.base import Base
from database.database import engine
import pytest
from database.database import SessionLocal


@pytest.fixture
def test_session():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)