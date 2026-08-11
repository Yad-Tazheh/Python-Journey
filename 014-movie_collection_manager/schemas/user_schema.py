from pydantic import BaseModel, ConfigDict

from schemas.review_schema import ReviewResponse


class UserCreate(BaseModel):
    username: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str

class UserWithReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    reviews: list["ReviewResponse"]