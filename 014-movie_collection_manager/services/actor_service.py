from models import Movie
from models.actor import Actor

from repositories.actor_repository import ActorRepository
from repositories.movie_repository import MovieRepository

from exceptions.actor_exceptions import (
    ActorAlreadyAssociatedException,
    ActorAlreadyExistsException,
    ActorNotFoundException,
    MovieAlreadyAssociatedException,
)

from exceptions.movie_exceptions import MovieNotFoundException


class ActorService:
    def __init__(
        self,
        actor_repository: ActorRepository,
        movie_repository: MovieRepository,
    ) -> None:
        self.actor_repository = actor_repository
        self.movie_repository = movie_repository

    def get_all(self) -> list[Actor]:
        return self.actor_repository.get_all()

    def get_by_id(self, actor_id: int) -> Actor:
        existing_actor = self.actor_repository.get_by_id(actor_id)

        if not existing_actor:
            raise ActorNotFoundException("Actor not found")

        return existing_actor

    def get_by_name(self, actor_name: str) -> Actor:
        existing_actor = self.actor_repository.get_by_name(actor_name)

        if not existing_actor:
            raise ActorNotFoundException("Actor not found")

        return existing_actor

    def create(self, actor: Actor) -> Actor:
        existing_actor = self.actor_repository.get_by_name(actor.name)

        if existing_actor:
            raise ActorAlreadyExistsException("Actor already exists")

        return self.actor_repository.create(actor)

    def update(
        self,
        actor_id: int,
        updated_actor: Actor,
    ) -> Actor:
        existing_actor = self.actor_repository.get_by_id(actor_id)

        if not existing_actor:
            raise ActorNotFoundException("Actor not found")

        existing_actor.name = updated_actor.name

        return self.actor_repository.update(existing_actor)

    def delete(self, actor_id: int) -> Actor:
        existing_actor = self.actor_repository.get_by_id(actor_id)

        if not existing_actor:
            raise ActorNotFoundException("Actor not found")

        self.actor_repository.delete(actor_id)

        return existing_actor

    def add_movie(
        self,
        actor_id: int,
        movie_id: int,
    ) -> Actor:
        existing_actor = self.actor_repository.get_by_id(actor_id)

        if not existing_actor:
            raise ActorNotFoundException("Actor not found")

        existing_movie = self.movie_repository.get_by_id(movie_id)

        if not existing_movie:
            raise MovieNotFoundException("Movie not found")

        if existing_movie in existing_actor.movies:
            raise MovieAlreadyAssociatedException(
                "Movie already associated with this actor"
            )

        existing_actor.movies.append(existing_movie)

        return self.actor_repository.update(existing_actor)

    def get_movies(self, actor_id: int) -> list[Movie]:
        existing_actor = self.actor_repository.get_by_id(actor_id)

        if not existing_actor:
            raise ActorNotFoundException("Actor not found")

        return existing_actor.movies