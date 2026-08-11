from pydantic import BaseModel, ConfigDict

from schemas import MovieResponse


class ActorCreate(BaseModel):
    name: str


class ActorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    actor_id: int
    name: str


class ActorWithMovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    actor_id: int
    name: str
    movies: list[MovieResponse]