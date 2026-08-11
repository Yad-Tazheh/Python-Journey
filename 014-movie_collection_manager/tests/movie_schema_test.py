import pytest
from pydantic import ValidationError

from models import Movie, Genre
from schemas import MovieUpdate, MovieCreate, MovieResponse
from schemas.genre_schema import GenreCreate, GenreResponse, GenreWithMovieResponse


def test_movie_schema(test_session):
    movie = MovieCreate(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )
    assert movie.title == "Test Movie"
    assert movie.description == "A test movie for unit testing"
    assert movie.release_date == "2023-01-01"

def test_movie_schema_required_fields(test_session):

    with pytest.raises(ValidationError):
         MovieCreate(
            description="A test movie for unit testing",
            release_date="2023-01-01"
        )


def test_movie_schema_update(test_session):

    movie = MovieUpdate(
        description="Test Movie2",
    )

    assert movie.description == "Test Movie2"
    assert movie.title is None
    assert movie.release_date is None


def test_movie_schema_response(test_session):
    movie = Movie(
        movie_id=1,
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )

    response = MovieResponse.model_validate(movie)

    assert response.movie_id == 1
    assert response.title == "Test Movie"
    assert response.description == "A test movie for unit testing"
    assert response.release_date == "2023-01-01"

