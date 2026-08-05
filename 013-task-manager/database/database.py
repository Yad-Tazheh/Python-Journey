from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/TaskManagerDB"
engine = create_engine(DATABASE_URL, echo=True) # connect sqlalchemy to postgres
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # replaces the cursor




def create_database():
    Base.metadata.create_all(bind=engine)

