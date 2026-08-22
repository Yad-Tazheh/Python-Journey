import pytest
from pydantic import ValidationError

from models import User, Review
from schemas import UserCreate, UserResponse
from schemas.user_schema import UserWithReviewResponse


def test_user_create_success():
    user = UserCreate(
        username="Ali",
        password="123456",
    )

    assert user.username == "Ali"



def test_user_create_failure():
    with pytest.raises(ValidationError):
        UserCreate()



def test_user_schema_response():
    user = User(
        user_id=1,
        username="Ali",
    )

    response = UserResponse.model_validate(user)

    assert response.username == "Ali"
    assert response.user_id == 1



def test_user_schema_with_review_response():
    user = User(
        user_id=1,
        username="Ali",
    )

    review1 = Review(
        review_id=1,
        content="Great movie!",
        rating=5,
        user=user,
        user_id=1,
        movie_id=1,
    )

    review2 = Review(
        review_id=2,
        content="Bad Movie",
        rating=1,
        user=user,
        user_id=1,
        movie_id=2,
    )


    response = UserWithReviewResponse.model_validate(user)

    assert response.username == "Ali"
    assert response.user_id == 1
    assert len(response.reviews) == 2
    assert response.reviews[0].content == "Great movie!"
    assert response.reviews[0].rating == 5
    assert response.reviews[1].content == "Bad Movie"
    assert response.reviews[1].rating == 1

