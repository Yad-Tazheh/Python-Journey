import pytest
from pydantic import ValidationError

from models import Movie
from models.actor import Actor
from schemas import ActorResponse, ActorCreate, ActorWithMovieResponse


def test_actor_schema_create_success():
    actor = ActorCreate(
        name='Ali',
    )
    assert actor.name == 'Ali'


def test_actor_schema_create_failure():

    with pytest.raises(ValidationError):
        ActorCreate()


def test_actor_schema_response_success():
    actor = Actor(
        actor_id=1,
        name='Ali',
    )

    response = ActorResponse.model_validate(actor)

    assert response.actor_id == 1
    assert response.name == 'Ali'


def test_actor_schema_with_movie_response_success():
    actor = Actor(
        actor_id=1,
        name='Ali',
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

    actor.movies.append(movie1)
    actor.movies.append(movie2)

    response = ActorWithMovieResponse.model_validate(actor)

    assert response.actor_id == 1
    assert response.name == "Ali"
    assert response.movies[0].title == "Test Movie"
    assert response.movies[1].title == "Test Movie2"
