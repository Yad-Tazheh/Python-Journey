import pytest

from exceptions.review_exceptions import ReviewNotFoundException
from exceptions.user_exceptions import UserNotFoundException
from exceptions.movie_exceptions import MovieNotFoundException
from models.review import Review
from models.user import User
from models.movie import Movie


def create_user(test_session, username="Ali"):
    user = User(username=username)

    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)

    return user


def create_movie(test_session, title="Test Movie"):
    movie = Movie(
        title=title,
        description="Test movie",
        release_date="2023-01-01",
    )

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    return movie


def create_review(
    review_service,
    test_session,
    username="Ali",
    title="Test Movie",
):
    user = create_user(test_session, username)
    movie = create_movie(test_session, title)

    review = Review(
        content="Great movie",
        rating=5,
        user_id=user.user_id,
        movie_id=movie.movie_id,
    )

    result = review_service.create(review)

    return result, user, movie


def test_service_get_all_reviews(
    review_service,
    test_session,
):
    review1, _, _ = create_review(
        review_service,
        test_session,
        username="Ali",
        title="Movie 1",
    )

    review2, _, _ = create_review(
        review_service,
        test_session,
        username="Reza",
        title="Movie 2",
    )

    result = review_service.get_all()

    assert len(result) == 2
    assert review1 in result
    assert review2 in result


def test_service_create_review(
    review_service,
    test_session,
):
    review, user, movie = create_review(
        review_service,
        test_session,
    )

    assert review.review_id is not None
    assert review.content == "Great movie"
    assert review.rating == 5
    assert review.user_id == user.user_id
    assert review.movie_id == movie.movie_id


def test_service_get_review_by_id_success(
    review_service,
    test_session,
):
    review, _, _ = create_review(
        review_service,
        test_session,
    )

    result = review_service.get_by_id(review.review_id)

    assert result.review_id == review.review_id
    assert result.content == "Great movie"
    assert result.rating == 5


def test_service_get_review_by_id_not_found(review_service):
    with pytest.raises(ReviewNotFoundException):
        review_service.get_by_id(9999)


def test_service_get_reviews_by_user(
    review_service,
    test_session,
):
    user = create_user(test_session, "Ali")

    movie1 = create_movie(test_session, "Movie 1")
    movie2 = create_movie(test_session, "Movie 2")

    review1 = Review(
        content="Great",
        rating=5,
        user_id=user.user_id,
        movie_id=movie1.movie_id,
    )

    review2 = Review(
        content="Good",
        rating=4,
        user_id=user.user_id,
        movie_id=movie2.movie_id,
    )

    review_service.create(review1)
    review_service.create(review2)

    result = review_service.get_by_user_id(user.user_id)

    assert len(result) == 2
    assert review1 in result
    assert review2 in result


def test_service_get_reviews_by_user_not_found(review_service):
    with pytest.raises(UserNotFoundException):
        review_service.get_by_user_id(9999)


def test_service_get_reviews_by_movie(
    review_service,
    test_session,
):
    movie = create_movie(test_session)

    user1 = create_user(test_session, "Ali")
    user2 = create_user(test_session, "Reza")

    review1 = Review(
        content="Amazing",
        rating=5,
        user_id=user1.user_id,
        movie_id=movie.movie_id,
    )

    review2 = Review(
        content="Good",
        rating=4,
        user_id=user2.user_id,
        movie_id=movie.movie_id,
    )

    review_service.create(review1)
    review_service.create(review2)

    result = review_service.get_by_movie_id(movie.movie_id)

    assert len(result) == 2
    assert review1 in result
    assert review2 in result


def test_service_get_reviews_by_movie_not_found(review_service):
    with pytest.raises(MovieNotFoundException):
        review_service.get_by_movie_id(9999)


def test_service_update_review_success(
    review_service,
    test_session,
):
    review, _, _ = create_review(
        review_service,
        test_session,
    )

    updated_review = Review(
        content="Updated review",
        rating=3,
    )

    result = review_service.update(
        review.review_id,
        updated_review,
    )

    assert result.review_id == review.review_id
    assert result.content == "Updated review"
    assert result.rating == 3


def test_service_update_review_not_found(review_service):
    updated_review = Review(
        content="Updated review",
        rating=3,
    )

    with pytest.raises(ReviewNotFoundException):
        review_service.update(
            9999,
            updated_review,
        )


def test_service_delete_review_success(
    review_service,
    test_session,
):
    review, _, _ = create_review(
        review_service,
        test_session,
    )

    deleted_review = review_service.delete(
        review.review_id,
    )

    assert deleted_review.review_id == review.review_id

    with pytest.raises(ReviewNotFoundException):
        review_service.get_by_id(review.review_id)


def test_service_delete_review_not_found(review_service):
    with pytest.raises(ReviewNotFoundException):
        review_service.delete(9999)