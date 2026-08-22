from models.user import User, UserRole

from exceptions.user_exceptions import UserAlreadyExistsException
from exceptions.auth_exceptions import InvalidCredentialsException

from repositories.user_repository import UserRepository
from utils.password import hash_password, verify_password
from utils.jwt import create_access_token


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository


    def register(
        self,
        username: str,
        password: str,
    ) -> User:
        existing_user = self.user_repository.get_by_username(username)

        if existing_user:
            raise UserAlreadyExistsException(
                "User already exists"
            )

        user = User(
            username=username,
            password_hash=hash_password(password),
            role=UserRole.USER,
        )

        return self.user_repository.create(user)


    def login(
        self,
        username: str,
        password: str,
    ) -> str:

        user = self.user_repository.get_by_username(username)

        if not user:
            raise InvalidCredentialsException(
                "Invalid username or password"
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsException(
                "Invalid username or password"
            )

        return create_access_token(
            {
                "sub": str(user.user_id),
                "username": user.username,
                "role": user.role.value,
            }
        )