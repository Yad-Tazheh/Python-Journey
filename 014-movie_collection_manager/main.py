from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import create_database

from exceptions.actor_exceptions import (
    ActorAlreadyAssociatedException,
    ActorAlreadyExistsException,
    ActorNotFoundException,
    MovieAlreadyAssociatedException,
)
from exceptions.exception_handlers import (
    actor_already_associated_handler,
    actor_already_exists_handler,
    actor_not_found_handler,
    genre_already_associated_handler,
    genre_not_found_handler,
    movie_already_associated_handler,
    movie_already_exists_handler,
    movie_not_found_handler,
    review_not_found_handler,
    user_not_found_handler,
)
from exceptions.genre_exceptions import (
    GenreAlreadyAssociatedException,
    GenreNotFoundException,
)
from exceptions.movie_exceptions import (
    MovieAlreadyExistsException,
    MovieNotFoundException,
)
from exceptions.review_exceptions import ReviewNotFoundException
from exceptions.user_exceptions import UserNotFoundException

from routers.actor_router import router as actor_router
from routers.genre_router import router as genre_router
from routers.movie_router import router as movie_router
from routers.review_router import router as review_router
from routers.user_router import router as user_router

# Import models so SQLAlchemy knows all tables and relationships.
import models.actor
import models.genre
import models.movie
import models.review
import models.user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)


## note: only for development/testing
## startup event is deprecated in newer FastAPI versions
# @app.on_event("startup")
# def startup():
#     create_database()


app.add_exception_handler(
    MovieNotFoundException,
    movie_not_found_handler,
)

app.add_exception_handler(
    MovieAlreadyExistsException,
    movie_already_exists_handler,
)

app.add_exception_handler(
    MovieAlreadyAssociatedException,
    movie_already_associated_handler,
)

app.add_exception_handler(
    ActorNotFoundException,
    actor_not_found_handler,
)

app.add_exception_handler(
    ActorAlreadyExistsException,
    actor_already_exists_handler,
)

app.add_exception_handler(
    ActorAlreadyAssociatedException,
    actor_already_associated_handler,
)

app.add_exception_handler(
    GenreNotFoundException,
    genre_not_found_handler,
)

app.add_exception_handler(
    GenreAlreadyAssociatedException,
    genre_already_associated_handler,
)

app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler,
)

app.add_exception_handler(
    ReviewNotFoundException,
    review_not_found_handler,
)


app.include_router(movie_router)
app.include_router(actor_router)
app.include_router(genre_router)
app.include_router(user_router)
app.include_router(review_router)