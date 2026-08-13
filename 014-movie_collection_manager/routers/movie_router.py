from fastapi import APIRouter, Depends

from dependencies import get_movie_service
from schemas.movie_schema import MovieResponse, MovieCreate, MovieUpdate
from services.movie_service import MovieService
from models.movie import Movie

# this is a container for routers related to Movie
# http method + URL = Action (don't use function names for the actions)
router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get("/", response_model=list[MovieResponse])
def get_all_movies(
        movie_service: MovieService = Depends(get_movie_service)
):
    return movie_service.get_all()


@router.post("/", response_model=MovieResponse)
def create_movie(
        movie: MovieCreate,
        movie_service: MovieService = Depends(get_movie_service)
):

    new_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date
    )
    return movie_service.create(new_movie)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_by_id(
        movie_id: int,
        movie_service: MovieService = Depends(get_movie_service)

):
    return movie_service.get_by_id(movie_id)


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
        movie_id: int,
        movie: MovieUpdate,
        movie_service: MovieService = Depends(get_movie_service)
):
    updated_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date
    )
    return movie_service.update(movie_id, updated_movie)

@router.delete("/{movie_id}", response_model=MovieResponse)
def delete_movie(
        movie_id: int,
        movie_service: MovieService = Depends(get_movie_service)
):
    return movie_service.delete(movie_id)

@router.get("/title/{title}", response_model=MovieResponse)
def get_movie_by_title(
        title: str,
        movie_service: MovieService = Depends(get_movie_service)
):
    return movie_service.get_by_title(title)