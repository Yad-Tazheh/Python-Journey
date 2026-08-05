from sqlalchemy.orm import DeclarativeBase

# this is a registry for SQLAlchemy such that it can manage the child classes metadata
class Base(DeclarativeBase):
    pass
