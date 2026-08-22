from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from utils.jwt import decode_access_token
from models.user import User, UserRole

from database.database import SessionLocal

from repositories.actor_repository import ActorRepository
from repositories.genre_repository import GenreRepository
from repositories.movie_repository import MovieRepository
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository

from services.actor_service import ActorService
from services.genre_serive import GenreService
from services.movie_service import MovieService
from services.review_service import ReviewService
from services.user_service import UserService
from services.auth_service import AuthService


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_movie_service(
    db: Session = Depends(get_session),
) -> MovieService:
    movie_repository = MovieRepository(db)
    actor_repository = ActorRepository(db)
    genre_repository = GenreRepository(db)

    return MovieService(
        movie_repository=movie_repository,
        actor_repository=actor_repository,
        genre_repository=genre_repository,
    )


def get_actor_service(
    db: Session = Depends(get_session),
) -> ActorService:
    actor_repository = ActorRepository(db)
    movie_repository = MovieRepository(db)

    return ActorService(
        actor_repository=actor_repository,
        movie_repository=movie_repository,
    )


def get_genre_service(
    db: Session = Depends(get_session),
) -> GenreService:
    genre_repository = GenreRepository(db)
    movie_repository = MovieRepository(db)

    return GenreService(
        genre_repository=genre_repository,
        movie_repository=movie_repository,
    )


def get_user_service(
    db: Session = Depends(get_session),
) -> UserService:
    user_repository = UserRepository(db)

    return UserService(
        user_repository=user_repository,
    )


def get_review_service(
    db: Session = Depends(get_session),
) -> ReviewService:
    review_repository = ReviewRepository(db)
    movie_repository = MovieRepository(db)
    user_repository = UserRepository(db)

    return ReviewService(
        review_repository=review_repository,
        user_repository=user_repository,
        movie_repository=movie_repository,
    )


def get_auth_service(
    db: Session = Depends(get_session),
) -> AuthService:
    user_repository = UserRepository(db)

    return AuthService(
        user_repository=user_repository,
    )


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> User:
    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_repository = UserRepository(db)

    user = user_repository.get_by_id(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def require_admin(
        current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user



def require_owner_or_admin(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> User:
    review_repository = ReviewRepository(db)

    review = review_repository.get_by_id(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    if (
        review.user_id != current_user.user_id
        and current_user.role != UserRole.ADMIN
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    return current_user

