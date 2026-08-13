from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from exceptions.genre_exceptions import GenreNotFoundException
from exceptions.movie_exceptions import MovieNotFoundException
from exceptions.actor_exceptions import ActorNotFoundException
from exceptions.review_exceptions import ReviewNotFoundException
from exceptions.user_exceptions import UserNotFoundException


def movie_not_found_handler(
        request: Request,
        exc: MovieNotFoundException
):
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)}
            )

def actor_not_found_handler(
        request: Request,
        exc: ActorNotFoundException

):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

def genre_not_found_handler(
        request: Request,
        exc: GenreNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

def review_not_found_handler(
        request: Request,
        exc: ReviewNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )