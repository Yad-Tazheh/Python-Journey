from fastapi import APIRouter, Depends

from dependencies import get_movie_service, require_admin
from models.movie import Movie
from models.user import User
from schemas.actor_schema import ActorResponse
from schemas.genre_schema import GenreResponse
from schemas.movie_schema import (
    MovieCreate,
    MovieResponse,
    MovieUpdate,
)
from services.movie_service import MovieService


# this is a container for routers related to Movie
# http method + URL = Action (don't use function names for the actions)
router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get("/", response_model=list[MovieResponse])
def get_all_movies(
    movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_all()


@router.post("/", response_model=MovieResponse)
def create_movie(
    movie: MovieCreate,
    movie_service: MovieService = Depends(get_movie_service),
    _: User = Depends(require_admin),
):
    new_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
    )

    return movie_service.create(new_movie)


@router.get("/title/{title}", response_model=MovieResponse)
def get_movie_by_title(
    title: str,
    movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_by_title(title)


@router.post(
    "/{movie_id}/actors/{actor_id}",
    response_model=MovieResponse,
)
def add_actor_to_movie(
    movie_id: int,
    actor_id: int,
    movie_service: MovieService = Depends(get_movie_service),
    _: User = Depends(require_admin),
):
    return movie_service.add_actor(movie_id, actor_id)


@router.get(
    "/{movie_id}/actors",
    response_model=list[ActorResponse],
)
def get_movie_actors(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_actors(movie_id)


@router.post(
    "/{movie_id}/genres/{genre_id}",
    response_model=MovieResponse,
)
def add_genre_to_movie(
    movie_id: int,
    genre_id: int,
    movie_service: MovieService = Depends(get_movie_service),
    _: User = Depends(require_admin),
):
    return movie_service.add_genre(movie_id, genre_id)


@router.get(
    "/{movie_id}/genres",
    response_model=list[GenreResponse],
)
def get_movie_genres(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_genres(movie_id)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_by_id(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_by_id(movie_id)


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    movie_service: MovieService = Depends(get_movie_service),
    _: User = Depends(require_admin),
):
    updated_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
    )

    return movie_service.update(movie_id, updated_movie)


@router.delete("/{movie_id}", response_model=MovieResponse)
def delete_movie(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service),
    _: User = Depends(require_admin),
):
    return movie_service.delete(movie_id)