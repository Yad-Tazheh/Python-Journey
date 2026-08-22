from models.user import User

from exceptions.user_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from repositories.user_repository import UserRepository

from utils.password import hash_password
from schemas.user_schema import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_all(self) -> list[User]:
        return self.user_repository.get_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException("User not found")

        return user

    def get_by_username(self, username: str) -> User:
        user = self.user_repository.get_by_username(username)

        if not user:
            raise UserNotFoundException("User not found")

        return user

    def create(self, user_data: UserCreate) -> User:
        existing_user = self.user_repository.get_by_username(user_data.username)

        if existing_user:
            raise UserAlreadyExistsException("User already exists")

        user = User(
            username=user_data.username,
            password_hash=hash_password(user_data.password),
        )

        return self.user_repository.create(user)


    def update(
        self,
        user_id: int,
        updated_user: User,
    ) -> User:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException("User not found")

        user.username = updated_user.username

        return self.user_repository.update(user)

    def delete(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException("User not found")

        self.user_repository.delete(user_id)

        return user