from models.user import User

from repositories.user_repository import UserRepository
from exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository


    def get_all(self) -> list[User]:
        return self.user_repository.get_all()

    def get_by_id(self, user_id: int) -> User:
        existing_user = self.user_repository.get_by_id(user_id)

        if not existing_user:
            raise UserNotFoundException('User not found')

        return existing_user

    def get_by_username(self, username: str) -> User:
        existing_user = self.user_repository.get_by_username(username)

        if not existing_user:
            raise UserNotFoundException('User not found')

        return existing_user

    def create(self, user: User) -> User:
        existing_user = self.user_repository.get_by_username(user.username)

        if existing_user:
            raise UserAlreadyExistsException('User already exists')

        return self.user_repository.create(user)

    def update(self, user_id: int, updated_user: User) -> User:
        existing_user = self.user_repository.get_by_id(user_id)

        if not existing_user:
            raise UserNotFoundException('User not found')

        existing_user.username = updated_user.username

        return self.user_repository.update(existing_user)

    def delete(self, user_id: int) -> User:
        existing_user = self.user_repository.get_by_id(user_id)

        if not existing_user:
            raise UserNotFoundException('User not found')

        self.user_repository.delete(user_id)

        return existing_user