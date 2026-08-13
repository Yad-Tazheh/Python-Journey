from contextlib import asynccontextmanager
from fastapi import FastAPI

from exceptions.user_exceptions import UserNotFoundException
from routers.movie_router import router as movie_router
from routers.actor_router import router as actor_router
from routers.genre_router import router as genre_router
from routers.user_router import router as user_router
from routers.review_router import router as review_router

from database.database import create_database

from exceptions.exception_handlers import movie_not_found_handler
from exceptions.exception_handlers import genre_not_found_handler
from exceptions.exception_handlers import actor_not_found_handler
from exceptions.exception_handlers import user_not_found_handler
from exceptions.exception_handlers import review_not_found_handler

from exceptions.movie_exceptions import MovieNotFoundException
from exceptions.actor_exceptions import ActorNotFoundException
from exceptions.genre_exceptions import GenreNotFoundException
from exceptions.user_exceptions import UserNotFoundException
from exceptions.review_exceptions import ReviewNotFoundException

import models.movie
import models.actor
import models.genre
import models.review
import models.user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield
app = FastAPI(lifespan=lifespan)


## note: only for development/testing
## startup event is deprecated in newer FastAPI versions
#@app.on_event("startup")
#def startup():
#    create_database()
#

app.add_exception_handler(
    MovieNotFoundException,
    movie_not_found_handler


)
app.add_exception_handler(
    ActorNotFoundException,
    actor_not_found_handler
)
app.add_exception_handler(
    GenreNotFoundException,
    genre_not_found_handler
)
app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler
)
app.add_exception_handler(
    ReviewNotFoundException,
    review_not_found_handler
)

app.include_router(movie_router)
app.include_router(actor_router)
app.include_router(genre_router)
app.include_router(user_router)
app.include_router(review_router)