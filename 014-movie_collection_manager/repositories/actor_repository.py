from sqlalchemy.orm import Session

from models import Actor

class ActorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Actor]:
        return self.db.query(Actor).all()

    def get_by_id(self, actor_id: int) -> Actor:
        return self.db.query(Actor).filter(Actor.actor_id == actor_id).first()

    def get_by_name(self, name: str) -> Actor:
        return self.db.query(Actor).filter(Actor.name == name).first()

    def create(self, actor: Actor) -> Actor:
        self.db.add(actor)
        self.db.commit()
        self.db.refresh(actor)

        return actor

    def update(self, actor: Actor) -> Actor:
        self.db.commit()
        self.db.refresh(actor)

        return actor

    def delete(self, actor_id: int) -> Actor:
        actor = self.get_by_id(actor_id)

        if actor:
            self.db.delete(actor)
            self.db.commit()

        return actor
