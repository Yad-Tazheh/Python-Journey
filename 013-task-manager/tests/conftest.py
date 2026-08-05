import pytest

from models.user import User
from models.task import Task
from models.project import Project

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database.database import Base
TEST_DATABASE_URL = ("postgresql+psycopg2://postgres:postgres@localhost:5432/TaskManagerDB_test")

test_engine = create_engine(TEST_DATABASE_URL,echo=True)


TestSessionLocal = sessionmaker(bind=test_engine,autoflush=False)


@pytest.fixture
def test_session():

    Base.metadata.create_all(bind=test_engine)

    session = TestSessionLocal()

    yield session

    session.rollback()
    session.close()

    Base.metadata.drop_all(bind=test_engine)