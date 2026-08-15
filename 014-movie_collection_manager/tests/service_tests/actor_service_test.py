import pytest

from models.actor import Actor
from models.movie import Movie

from repositories.actor_repository import ActorRepository
from repositories.movie_repository import MovieRepository

from services.actor_service import ActorService

from exceptions.actor_exceptions import (
    ActorAlreadyExistsException,
    ActorNotFoundException,
    MovieAlreadyAssociatedException,
)

from exceptions.movie_exceptions import MovieNotFoundException


@pytest.fixture
def actor_service(test_session):
    actor_repository = ActorRepository(test_session)
    movie_repository = MovieRepository(test_session)

    return ActorService(
        actor_repository=actor_repository,
        movie_repository=movie_repository,
    )


def test_service_get_all_actors(actor_service):
    actor1 = Actor(name="Tom Hanks")
    actor2 = Actor(name="Tom Cruise")

    actor_service.create(actor1)
    actor_service.create(actor2)

    result = actor_service.get_all()

    assert len(result) == 2
    assert {actor.name for actor in result} == {
        "Tom Hanks",
        "Tom Cruise",
    }


def test_service_get_actor_by_id_success(actor_service):
    actor = Actor(name="Tom Hanks")

    actor_service.create(actor)

    result = actor_service.get_by_id(actor.actor_id)

    assert result.actor_id == actor.actor_id
    assert result.name == "Tom Hanks"


def test_service_get_actor_by_id_not_found(actor_service):
    with pytest.raises(ActorNotFoundException):
        actor_service.get_by_id(9999)


def test_service_get_actor_by_name_success(actor_service):
    actor = Actor(name="Tom Hanks")

    actor_service.create(actor)

    result = actor_service.get_by_name("Tom Hanks")

    assert result.actor_id == actor.actor_id
    assert result.name == "Tom Hanks"


def test_service_get_actor_by_name_not_found(actor_service):
    with pytest.raises(ActorNotFoundException):
        actor_service.get_by_name("Unknown Actor")


def test_service_create_actor(actor_service):
    actor = Actor(name="Tom Hanks")

    result = actor_service.create(actor)

    assert result.actor_id is not None
    assert result.name == "Tom Hanks"


def test_service_create_duplicate_actor(actor_service):
    actor1 = Actor(name="Tom Hanks")
    actor2 = Actor(name="Tom Hanks")

    actor_service.create(actor1)

    with pytest.raises(ActorAlreadyExistsException):
        actor_service.create(actor2)


def test_service_update_actor(actor_service):
    actor = Actor(name="Tom Hanks")

    actor_service.create(actor)

    updated_actor = Actor(name="Tom Cruise")

    result = actor_service.update(
        actor.actor_id,
        updated_actor,
    )

    assert result.actor_id == actor.actor_id
    assert result.name == "Tom Cruise"


def test_service_update_actor_not_found(actor_service):
    updated_actor = Actor(name="Tom Cruise")

    with pytest.raises(ActorNotFoundException):
        actor_service.update(
            9999,
            updated_actor,
        )


def test_service_delete_actor(actor_service):
    actor = Actor(name="Tom Hanks")

    actor_service.create(actor)

    result = actor_service.delete(actor.actor_id)

    assert result.actor_id == actor.actor_id
    assert result.name == "Tom Hanks"

    with pytest.raises(ActorNotFoundException):
        actor_service.get_by_id(actor.actor_id)


def test_service_delete_actor_not_found(actor_service):
    with pytest.raises(ActorNotFoundException):
        actor_service.delete(9999)


def test_service_add_movie_to_actor(actor_service, test_session):
    actor = Actor(name="Tom Hanks")
    movie = Movie(
        title="Forrest Gump",
        description="A test movie",
        release_date="1994-07-06",
    )

    actor_service.create(actor)

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    result = actor_service.add_movie(
        actor.actor_id,
        movie.movie_id,
    )

    assert result.actor_id == actor.actor_id
    assert len(result.movies) == 1
    assert result.movies[0].movie_id == movie.movie_id


def test_service_add_movie_actor_not_found(actor_service, test_session):
    movie = Movie(
        title="Forrest Gump",
        description="A test movie",
        release_date="1994-07-06",
    )

    test_session.add(movie)
    test_session.commit()

    with pytest.raises(ActorNotFoundException):
        actor_service.add_movie(
            9999,
            movie.movie_id,
        )


def test_service_add_movie_movie_not_found(actor_service):
    actor = Actor(name="Tom Hanks")

    actor_service.create(actor)

    with pytest.raises(MovieNotFoundException):
        actor_service.add_movie(
            actor.actor_id,
            9999,
        )


def test_service_add_movie_already_associated(
    actor_service,
    test_session,
):
    actor = Actor(name="Tom Hanks")

    movie = Movie(
        title="Forrest Gump",
        description="A test movie",
        release_date="1994-07-06",
    )

    actor_service.create(actor)

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    actor_service.add_movie(
        actor.actor_id,
        movie.movie_id,
    )

    with pytest.raises(MovieAlreadyAssociatedException):
        actor_service.add_movie(
            actor.actor_id,
            movie.movie_id,
        )


def test_service_get_movies(actor_service, test_session):
    actor = Actor(name="Tom Hanks")

    movie = Movie(
        title="Forrest Gump",
        description="A test movie",
        release_date="1994-07-06",
    )

    actor_service.create(actor)

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    actor_service.add_movie(
        actor.actor_id,
        movie.movie_id,
    )

    result = actor_service.get_movies(actor.actor_id)

    assert len(result) == 1
    assert result[0].movie_id == movie.movie_id
    assert result[0].title == "Forrest Gump"


def test_service_get_movies_actor_not_found(actor_service):
    with pytest.raises(ActorNotFoundException):
        actor_service.get_movies(9999)