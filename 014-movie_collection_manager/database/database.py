import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
if DB_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_database():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()