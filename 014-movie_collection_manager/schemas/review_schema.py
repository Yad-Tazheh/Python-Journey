from pydantic import BaseModel, ConfigDict, Field

from schemas.movie_schema import MovieResponse


class ReviewCreate(BaseModel):
    content: str
    rating: int = Field(ge=1, le=10)
    user_id: int
    movie_id: int

class ReviewUpdate(BaseModel):
    content: str
    rating: int = Field(ge=1, le=10)

class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: int
    content: str
    rating: int
    user_id: int
    movie_id: int

class ReviewWithMovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: int
    content: str
    rating: int = Field(ge=1, le=10)
    movie: MovieResponse

