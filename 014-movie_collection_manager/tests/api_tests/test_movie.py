
def test_get_all_movies(client):
    response = client.get("/movies/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_movie(client):
    response = client.post(
        "/movies/",
        json={
            "title": "Test movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test movie"
    assert data["description"] == "A test movie"
    assert data["release_date"] == "2023-01-01"


def test_update_movie(client):
    response = client.post(
        "/movies/",
        json={
            "title": "Old title",
            "description": "Old description",
            "release_date": "2023-01-01",
        },
    )

    assert response.status_code == 200

    movie_id = response.json()["movie_id"]

    response = client.put(
        f"/movies/{movie_id}",
        json={
            "title": "New title",
            "description": "New description",
            "release_date": "2024-01-01",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["movie_id"] == movie_id
    assert data["title"] == "New title"
    assert data["description"] == "New description"
    assert data["release_date"] == "2024-01-01"



def test_delete_movie(client):
    response = client.post(
        "/movies/",
        json={
            "title": "Test movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        }
    )

    assert response.status_code == 200

    movie_id = response.json()["movie_id"]
    response = client.delete(f"/movies/{movie_id}")

    assert response.status_code == 200


    data = response.json()
    assert data["movie_id"] == movie_id

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_delete_movie_not_found(client):
    response = client.delete("/movies/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_get_movie_by_title(client):
    response = client.post(
        "/movies/",
        json={
            "title": "Inception",
            "description": "A science fiction movie",
            "release_date": "2010-07-16",
        },
    )

    assert response.status_code == 200

    response = client.get("/movies/title/Inception")

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Inception"
    assert data["description"] == "A science fiction movie"
    assert data["release_date"] == "2010-07-16"


def test_get_movie_by_title_not_found(client):
    response = client.get("/movies/title/Unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_add_actor_to_movie(client):
    # Create movie
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200

    movie_id = movie_response.json()["movie_id"]

    # Create actor
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200

    actor_id = actor_response.json()["actor_id"]

    # Add actor to movie
    response = client.post(
        f"/movies/{movie_id}/actors/{actor_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["movie_id"] == movie_id
    assert data["title"] == "Test Movie"


def test_add_actor_to_movie_movie_not_found(client):
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200

    actor_id = actor_response.json()["actor_id"]

    response = client.post(
        f"/movies/9999/actors/{actor_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_add_actor_to_movie_actor_not_found(client):
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200

    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/movies/{movie_id}/actors/9999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"


def test_add_actor_to_movie_already_associated(client):
    # Create movie
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200

    movie_id = movie_response.json()["movie_id"]

    # Create actor
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200

    actor_id = actor_response.json()["actor_id"]

    # First association
    response = client.post(
        f"/movies/{movie_id}/actors/{actor_id}"
    )

    assert response.status_code == 200

    # Second association
    response = client.post(
        f"/movies/{movie_id}/actors/{actor_id}"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Actor already associated with the movie"
    )


def test_get_movie_actors(client):
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200
    movie_id = movie_response.json()["movie_id"]

    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200
    actor_id = actor_response.json()["actor_id"]

    response = client.post(
        f"/movies/{movie_id}/actors/{actor_id}"
    )

    assert response.status_code == 200

    response = client.get(
        f"/movies/{movie_id}/actors"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["actor_id"] == actor_id
    assert data[0]["name"] == "Tom Hanks"


def test_get_movie_actors_movie_not_found(client):
    response = client.get("/movies/9999/actors")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_add_and_get_movie_genres(client):
    # Create movie
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200

    movie_id = movie_response.json()["movie_id"]

    # Create genre
    genre_response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert genre_response.status_code == 200

    genre_id = genre_response.json()["genre_id"]

    # Add genre to movie
    response = client.post(
        f"/movies/{movie_id}/genres/{genre_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["movie_id"] == movie_id
    assert data["title"] == "Test Movie"

    # Get movie genres
    response = client.get(
        f"/movies/{movie_id}/genres"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["genre_id"] == genre_id
    assert data[0]["name"] == "Action"


def test_get_movie_genres_movie_not_found(client):
    response = client.get("/movies/9999/genres")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"



def test_add_genre_to_movie_genre_not_found(client):
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200

    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/movies/{movie_id}/genres/9999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Genre not found"


def test_add_genre_to_movie_already_associated(client):
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "release_date": "2023-01-01",
        },
    )

    assert movie_response.status_code == 200

    movie_id = movie_response.json()["movie_id"]

    genre_response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert genre_response.status_code == 200

    genre_id = genre_response.json()["genre_id"]

    # First association
    response = client.post(
        f"/movies/{movie_id}/genres/{genre_id}"
    )

    assert response.status_code == 200

    # Duplicate association
    response = client.post(
        f"/movies/{movie_id}/genres/{genre_id}"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Genre already associated with the movie"
    )


def test_get_movie_by_id(client, test_movie):
    response = client.get(f"/movies/{test_movie.movie_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["movie_id"] == test_movie.movie_id
    assert data["title"] == "Test Movie"
    assert data["description"] == "A test movie"
    assert data["release_date"] == "2023-01-01"


def test_get_movie_by_id_not_found(client):
    response = client.get("/movies/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_create_movie_duplicate_title(client):
    movie_data = {
        "title": "Inception",
        "description": "A movie",
        "release_date": "2010-07-16",
    }

    response = client.post("/movies/", json=movie_data)

    assert response.status_code == 200

    response = client.post("/movies/", json=movie_data)

    assert response.status_code == 409
    assert response.json()["detail"] == "Movie already exists"


def test_update_movie_not_found(client):
    response = client.put(
        "/movies/9999",
        json={
            "title": "New title",
            "description": "New description",
            "release_date": "2024-01-01",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"