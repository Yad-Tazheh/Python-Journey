from pydantic import BaseModel, ConfigDict

from schemas import MovieResponse


class GenreCreate(BaseModel):
    name : str

class GenreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    genre_id: int
    name: str

class GenreUpdate(BaseModel):
    name: str

class GenreWithMovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    genre_id: int
    name: str
    movies: list[MovieResponse]

