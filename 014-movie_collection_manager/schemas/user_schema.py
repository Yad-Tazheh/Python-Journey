from pydantic import BaseModel, ConfigDict, Field

from schemas.review_schema import ReviewResponse


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=6,
        max_length=50,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    user_id: int
    username: str


class UserUpdate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )


class UserWithReviewResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    user_id: int
    username: str
    reviews: list["ReviewResponse"]


UserWithReviewResponse.model_rebuild()