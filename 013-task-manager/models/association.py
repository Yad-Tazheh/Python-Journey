from sqlalchemy import Table, Column, String, Integer, ForeignKey

from database.base import Base


project_users = Table(
    "project_users",
    Base.metadata,

    Column(
        "project_id",
        String,
        ForeignKey("projects.project_id"),
        primary_key=True
    ),

    Column(
        "user_id",
        Integer,
        ForeignKey("users.user_id"),
        primary_key=True
    )
)