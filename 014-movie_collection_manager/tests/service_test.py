import pytest
from models import Movie, movie
from services.movie_service import MovieService
from repositories.movie_repository import MovieRepository


def test_service_create_movie(test_session):

    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )


    movie_service.create(movie)
    saved_movie = movie_service.get_by_id(movie.movie_id)

    assert saved_movie.title == movie.title

def test_service_movie_duplicate(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    movie1 = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )

    movie2 = Movie(
        title="Test Movie",
        description="Another test movie for unit testing",
        release_date="2024-01-01"
    )

    movie_service.create(movie1)

    with pytest.raises(Exception):
        movie_service.create(movie2)


def test_service_get_movie_by_id_success(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)
    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )

    movie_service.create(movie)
    saved_movie = movie_service.get_by_id(movie.movie_id)
    assert saved_movie.title == movie.title

def test_service_get_movie_by_id_not_found(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    with pytest.raises(Exception):
        movie_service.get_by_id(8888)


def test_service_get_movie_by_title(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )

    movie_service.create(movie)

    saved_movie = movie_service.get_by_title(movie.title)

    assert saved_movie.title == movie.title


def test_service_get_by_title_not_found(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    with pytest.raises(Exception):
        movie_service.get_by_title("a test title")


def test_service_get_all(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    movie1 = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )
    movie2 = Movie(
        title="Test Movie2",
        description="Another test movie for unit testing",
        release_date="2024-01-01"
    )

    movie3 = Movie(
        title="Test Movie3",
        description="Another test movie for unit testing",
        release_date="2025-01-01"
    )
    movie_service.create(movie1)
    movie_service.create(movie2)
    movie_service.create(movie3)

    result = [movie.title for movie in movie_service.get_all()]

    assert sorted(result) == ["Test Movie", "Test Movie2", "Test Movie3"]


def test_service_update_success(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )
    updated_movie = Movie(
        title="Test Movie2",
        description="Another test movie for unit testing",
        release_date="2024-01-01"
    )
    movie_service.create(movie)
    movie_service.update(movie.movie_id, updated_movie)

    assert (movie_service.get_by_id(movie.movie_id).title == updated_movie.title)
    assert (movie_service.get_by_id(movie.movie_id).description == updated_movie.description)
    assert (movie_service.get_by_id(movie.movie_id).release_date == updated_movie.release_date)

def test_service_update_fail(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    updated_movie = Movie(
        title="Test Movie2",
        description="Another test movie for unit testing",
        release_date="2023-01-01"
    )

    with pytest.raises(Exception):
        movie_service.update(8888, updated_movie)

def test_service_delete_successfully(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    movie = Movie(
        title="Test Movie",
        description="A test movie for unit testing",
        release_date="2023-01-01"
    )

    movie_service.create(movie)
    movie_service.delete(movie.movie_id)

    with pytest.raises(Exception):
        movie_service.get_by_id(movie.movie_id)


def test_service_delete_fail(test_session):
    repo = MovieRepository(test_session)
    movie_service = MovieService(repo)

    with pytest.raises(Exception):
        movie_service.delete(8888)

