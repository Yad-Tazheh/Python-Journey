from pydantic import BaseModel, ConfigDict


class MovieCreate(BaseModel):
    title: str
    description: str
    release_date: str

class MovieUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    release_date: str | None = None

class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movie_id: int
    title: str
    description: str
    release_date: str