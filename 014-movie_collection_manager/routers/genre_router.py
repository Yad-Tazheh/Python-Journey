from fastapi import APIRouter, Depends

from dependencies import get_genre_service
from models import Genre
from schemas.genre_schema import (
    GenreCreate,
    GenreResponse,
    GenreUpdate,
)
from schemas.movie_schema import MovieResponse
from services.genre_serive import GenreService


router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


@router.get("/", response_model=list[GenreResponse])
def get_all_genres(
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.get_all()


@router.post("/", response_model=GenreResponse)
def create_genre(
    genre: GenreCreate,
    genre_service: GenreService = Depends(get_genre_service),
):
    new_genre = Genre(
        name=genre.name,
    )

    return genre_service.create(new_genre)


@router.get("/name/{genre_name}", response_model=GenreResponse)
def get_genre_by_name(
    genre_name: str,
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.get_by_name(genre_name)


@router.post(
    "/{genre_id}/movies/{movie_id}",
    response_model=GenreResponse,
)
def add_movie_to_genre(
    genre_id: int,
    movie_id: int,
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.add_movie(genre_id, movie_id)


@router.get(
    "/{genre_id}/movies",
    response_model=list[MovieResponse],
)
def get_genre_movies(
    genre_id: int,
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.get_movies(genre_id)


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre_by_id(
    genre_id: int,
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.get_by_id(genre_id)


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: int,
    genre: GenreUpdate,
    genre_service: GenreService = Depends(get_genre_service),
):
    updated_genre = Genre(
        name=genre.name,
    )

    return genre_service.update(genre_id, updated_genre)


@router.delete("/{genre_id}", response_model=GenreResponse)
def delete_genre(
    genre_id: int,
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.delete(genre_id)