
from fastapi import APIRouter, Depends

from dependencies import get_actor_service

from schemas.actor_schema import ActorResponse, ActorCreate, ActorWithMovieResponse, ActorUpdate
from services.actor_service import ActorService
from models.actor import Actor


router = APIRouter(
    prefix="/actors",
    tags=["Actors"],
)

@router.get("/", response_model=list[ActorResponse])
def get_all_actors(
        actor_service: ActorService = Depends(get_actor_service)
):
    return actor_service.get_all()

@router.post("/", response_model=ActorWithMovieResponse)
def create_actor(
        actor: ActorCreate,
        actor_service: ActorService = Depends(get_actor_service)
):
    new_actor = Actor(name=actor.name)
    return actor_service.create(new_actor)

@router.get("/{actor_id}", response_model=ActorWithMovieResponse)
def get_actor_by_id(
        actor_id: int,
        actor_service: ActorService = Depends(get_actor_service)
):
    return actor_service.get_by_id(actor_id)


@router.put("/{actor_id}", response_model=ActorWithMovieResponse)
def update_actor(
        actor_id: int,
        actor: ActorUpdate,
        actor_service: ActorService = Depends(get_actor_service)
):
    updated_actor = Actor(
        name = actor.name,
    )
    return actor_service.update(actor_id, updated_actor)


@router.delete("/{actor_id}", response_model=ActorWithMovieResponse)
def delete_actor(
        actor_id: int,
        actor_service: ActorService = Depends(get_actor_service)
):
    return actor_service.delete(actor_id)