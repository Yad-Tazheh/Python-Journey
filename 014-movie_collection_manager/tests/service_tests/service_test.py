import pytest

from exceptions.movie_exceptions import (
    MovieAlreadyExistsException,
    MovieNotFoundException,
)
from models import Movie
from repositories.actor_repository import ActorRepository
from repositories.genre_repository import GenreRepository
from repositories.movie_repository import MovieRepository
from services.movie_service import MovieService


@pytest.fixture
def movie_service(test_session):
    movie_repository = MovieRepository(test_session)
    actor_repository = ActorRepository(test_session)
    genre_repository = GenreRepository(test_session)

    return MovieService(
        movie_repository=movie_repository,
        actor_repository=actor_repository,
        genre_repository=genre_repository,
    )


def test_service_create_movie(movie_service):
    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    movie_service.create(movie)
    saved_movie = movie_service.get_by_id(movie.movie_id)

    assert saved_movie.title == movie.title


def test_service_movie_duplicate(movie_service):
    movie1 = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    movie2 = Movie(
        title="Test Movie",
        description="Another test movie for unit testing",
        release_date="2024-01-01",
    )

    movie_service.create(movie1)

    with pytest.raises(MovieAlreadyExistsException):
        movie_service.create(movie2)


def test_service_get_movie_by_id_success(movie_service):
    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    movie_service.create(movie)
    saved_movie = movie_service.get_by_id(movie.movie_id)

    assert saved_movie.title == movie.title


def test_service_get_movie_by_id_not_found(movie_service):
    with pytest.raises(MovieNotFoundException):
        movie_service.get_by_id(8888)


def test_service_get_movie_by_title(movie_service):
    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    movie_service.create(movie)

    saved_movie = movie_service.get_by_title(movie.title)

    assert saved_movie.title == movie.title


def test_service_get_by_title_not_found(movie_service):
    with pytest.raises(MovieNotFoundException):
        movie_service.get_by_title("a test title")


def test_service_get_all(movie_service):
    movie1 = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    movie2 = Movie(
        title="Test Movie2",
        description="Another test movie for unit testing",
        release_date="2024-01-01",
    )

    movie3 = Movie(
        title="Test Movie3",
        description="Another test movie for unit testing",
        release_date="2025-01-01",
    )

    movie_service.create(movie1)
    movie_service.create(movie2)
    movie_service.create(movie3)

    result = [
        movie.title
        for movie in movie_service.get_all()
    ]

    assert sorted(result) == [
        "Test Movie",
        "Test Movie2",
        "Test Movie3",
    ]


def test_service_update_success(movie_service):
    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    updated_movie = Movie(
        title="Test Movie2",
        description="Another test movie for unit testing",
        release_date="2024-01-01",
    )

    movie_service.create(movie)
    movie_service.update(movie.movie_id, updated_movie)

    saved_movie = movie_service.get_by_id(movie.movie_id)

    assert saved_movie.title == updated_movie.title
    assert saved_movie.description == updated_movie.description
    assert saved_movie.release_date == updated_movie.release_date


def test_service_update_fail(movie_service):
    updated_movie = Movie(
        title="Test Movie2",
        description="Another test movie for unit testing",
        release_date="2023-01-01",
    )

    with pytest.raises(MovieNotFoundException):
        movie_service.update(8888, updated_movie)


def test_service_delete_successfully(movie_service):
    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01",
    )

    movie_service.create(movie)
    movie_service.delete(movie.movie_id)

    with pytest.raises(MovieNotFoundException):
        movie_service.get_by_id(movie.movie_id)


def test_service_delete_fail(movie_service):
    with pytest.raises(MovieNotFoundException):
        movie_service.delete(8888)