import pytest

from models import Review, Movie, User
from schemas import ReviewCreate, ReviewResponse, ReviewWithMovieResponse
from schemas.user_schema import UserWithReviewResponse


def test_review_schema_create():
    review = Review(
        review_id = 1,
        content = "This is a review.",
        rating = 7,
        user_id = 2,
        movie_id = 3,
    )

    response = ReviewResponse.model_validate(review)

    assert response.review_id == 1
    assert response.user_id == 2
    assert response.movie_id == 3
    assert review.content == "This is a review."
    assert review.rating == 7


def test_review_with_movie_response():
    movie = Movie(
        movie_id = 1,
        title = "Movie title",
        description = "Movie description",
        release_date="2024-01-01"
    )
    review = Review(
        review_id = 1,
        content = "This is a review.",
        rating = 7,
        movie = movie,
    )
    response = ReviewWithMovieResponse.model_validate(review)

    assert response.review_id == 1
    assert response.content == "This is a review."
    assert response.rating == 7
    assert response.movie.movie_id == 1
    assert response.movie.title == "Movie title"
    assert response.movie.description == "Movie description"
    assert response.movie.release_date == "2024-01-01"

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

    assert response.user_id == 1
    assert response.username == "Ali"
    assert len(response.reviews) == 2

    assert response.reviews[0].content == "Great movie!"
    assert response.reviews[0].rating == 5

    assert response.reviews[1].content == "Bad Movie"
    assert response.reviews[1].rating == 1









