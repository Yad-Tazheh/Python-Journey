import pytest
from pydantic import ValidationError

from models import Genre, Movie
from schemas import GenreCreate, GenreResponse, GenreWithMovieResponse


def test_genre_schema_create_valid(test_session):
    genre = GenreCreate(
        name="Test Genre",
    )

    assert genre.name == "Test Genre"

def test_genre_schema_create_invalid(test_session):
    with pytest.raises(ValidationError):
        GenreCreate()

def test_genre_schema_response(test_session):
    genre = GenreResponse(
        genre_id=1,
        name="Test Genre",
    )

    response = GenreResponse.model_validate(genre)

    assert response.genre_id == 1
    assert response.name == "Test Genre"


def test_genre_schema_with_movie_response():
    genre = Genre(
        genre_id=1,
        name="Test Genre",
    )

    movie1 = Movie(
        movie_id=1,
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )
    movie2 = Movie(
        movie_id=2,
        title="Test Movie2",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )


    genre.movies.append(movie1)
    genre.movies.append(movie2)

    response = GenreWithMovieResponse.model_validate(genre)

    assert response.genre_id == 1
    assert response.name == "Test Genre"
    assert len(response.movies) == 2
    assert response.movies[0].title == "Test Movie"
    assert response.movies[1].title == "Test Movie2"
