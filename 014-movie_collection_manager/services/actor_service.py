from models.actor import Actor

from repositories.actor_repository import ActorRepository
from exceptions.actor_exceptions import ActorAlreadyExistsException, ActorNotFoundException


class ActorService:
    def __init__(self, actor_repository: ActorRepository) -> None:
        self.actor_repository = actor_repository

    def get_all(self):
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
        existing_actor =  self.actor_repository.get_by_name(actor.name)

        if existing_actor:
            raise ActorAlreadyExistsException("Actor already exists")

        return self.actor_repository.create(actor)

    def update(self, actor_id: int, updated_actor: Actor) -> Actor:
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




