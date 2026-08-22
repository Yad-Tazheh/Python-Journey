from models import Review


def test_get_all_reviews(client):
    response = client.get("/reviews/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_review(client, test_user, test_movie):
    response = client.post(
        "/reviews/",
        json={
            "content": "A good movie",
            "rating": 5,
            "movie_id": test_movie.movie_id,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "A good movie"
    assert data["rating"] == 5
    assert data["user_id"] is not None
    assert data["movie_id"] == test_movie.movie_id


def test_create_review_with_invalid_rating(client, test_movie):
    response = client.post(
        "/reviews/",
        json={
            "content": "A good movie",
            "rating": 11,
            "movie_id": test_movie.movie_id,
        },
    )

    assert response.status_code == 422


def test_create_review_with_movie_not_found(client):
    response = client.post(
        "/reviews/",
        json={
            "content": "A good movie",
            "rating": 5,
            "movie_id": 9999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_get_review_by_id(client, test_session, test_user, test_movie):
    review = Review(
        content="A good movie",
        rating=6,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    test_session.add(review)
    test_session.commit()
    test_session.refresh(review)

    response = client.get(f"/reviews/{review.review_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["review_id"] == review.review_id
    assert data["content"] == "A good movie"
    assert data["rating"] == 6


def test_get_review_by_id_not_found(client):
    response = client.get("/reviews/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"


def test_get_reviews_by_user(client, test_session, test_user, test_movie):
    review1 = Review(
        content="A good movie",
        rating=5,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    review2 = Review(
        content="An excellent movie",
        rating=9,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    test_session.add_all([review1, review2])
    test_session.commit()

    response = client.get(
        f"/reviews/user/{test_user.user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(
        item["user_id"] == test_user.user_id
        for item in data
    )


def test_get_reviews_by_user_not_found(client):
    response = client.get("/reviews/user/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_reviews_by_movie(client, test_session, test_user, test_movie):
    review1 = Review(
        content="Great movie",
        rating=9,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    review2 = Review(
        content="Nice movie",
        rating=8,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    test_session.add_all([review1, review2])
    test_session.commit()

    response = client.get(
        f"/reviews/movie/{test_movie.movie_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(
        item["movie_id"] == test_movie.movie_id
        for item in data
    )


def test_get_reviews_by_movie_not_found(client):
    response = client.get("/reviews/movie/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_update_review(client, test_session, test_user, test_movie):
    review = Review(
        content="Old content",
        rating=4,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    test_session.add(review)
    test_session.commit()
    test_session.refresh(review)

    response = client.put(
        f"/reviews/{review.review_id}",
        json={
            "content": "Updated content",
            "rating": 9,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["review_id"] == review.review_id
    assert data["content"] == "Updated content"
    assert data["rating"] == 9


def test_update_review_not_found(client):
    response = client.put(
        "/reviews/9999",
        json={
            "content": "Updated content",
            "rating": 9,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"


def test_delete_review(client, test_session, test_user, test_movie):
    review = Review(
        content="A good movie",
        rating=8,
        user_id=test_user.user_id,
        movie_id=test_movie.movie_id,
    )

    test_session.add(review)
    test_session.commit()
    test_session.refresh(review)

    response = client.delete(
        f"/reviews/{review.review_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["review_id"] == review.review_id
    assert data["content"] == "A good movie"

    deleted_review = (
        test_session.query(Review)
        .filter(
            Review.review_id == review.review_id
        )
        .first()
    )

    assert deleted_review is None


def test_delete_review_not_found(client):
    response = client.delete("/reviews/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"