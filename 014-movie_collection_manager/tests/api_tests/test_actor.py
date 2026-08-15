
def test_get_all_actors(client):
    response = client.get("/actors/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_actor(client):
    response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Tom Hanks"


def test_get_actor_by_id(client):
    response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert response.status_code == 200

    actor_id = response.json()["actor_id"]

    response = client.get(f"/actors/{actor_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["actor_id"] == actor_id
    assert data["name"] == "Tom Hanks"


def test_get_actor_by_id_not_found(client):
    response = client.get("/actors/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"


def test_update_actor(client):
    response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert response.status_code == 200

    actor_id = response.json()["actor_id"]

    response = client.put(
        f"/actors/{actor_id}",
        json={
            "name": "Tom Cruise",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["actor_id"] == actor_id
    assert data["name"] == "Tom Cruise"


def test_update_actor_not_found(client):
    response = client.put(
        "/actors/9999",
        json={
            "name": "Tom Cruise",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"


def test_delete_actor(client):
    response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert response.status_code == 200

    actor_id = response.json()["actor_id"]

    response = client.delete(f"/actors/{actor_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["actor_id"] == actor_id
    assert data["name"] == "Tom Hanks"

    # Verify actor was deleted
    response = client.get(f"/actors/{actor_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"


def test_create_actor_duplicate_name(client):
    actor_data = {
        "name": "Tom Hanks",
    }

    response = client.post("/actors/", json=actor_data)

    assert response.status_code == 200

    response = client.post("/actors/", json=actor_data)

    assert response.status_code == 409
    assert response.json()["detail"] == "Actor already exists"


def test_create_actor_duplicate_name(client):
    actor_data = {
        "name": "Tom Hanks",
    }

    response = client.post(
        "/actors/",
        json=actor_data,
    )

    assert response.status_code == 200

    response = client.post(
        "/actors/",
        json=actor_data,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Actor already exists"


def test_get_actor_by_name(client):
    response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert response.status_code == 200

    response = client.get("/actors/name/Tom Hanks")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Tom Hanks"


def test_get_actor_by_name_not_found(client):
    response = client.get("/actors/name/Unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"


def test_add_movie_to_actor(client):
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200
    actor_id = actor_response.json()["actor_id"]

    movie_response = client.post(
        "/movies/",
        json={
            "title": "Forrest Gump",
            "description": "A movie",
            "release_date": "1994-07-06",
        },
    )

    assert movie_response.status_code == 200
    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/actors/{actor_id}/movies/{movie_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["actor_id"] == actor_id
    assert data["name"] == "Tom Hanks"


def test_add_movie_to_actor_actor_not_found(client):
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Forrest Gump",
            "description": "A movie",
            "release_date": "1994-07-06",
        },
    )

    assert movie_response.status_code == 200
    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/actors/9999/movies/{movie_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"


def test_add_movie_to_actor_movie_not_found(client):
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200
    actor_id = actor_response.json()["actor_id"]

    response = client.post(
        f"/actors/{actor_id}/movies/9999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


def test_add_movie_to_actor_already_associated(client):
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200
    actor_id = actor_response.json()["actor_id"]

    movie_response = client.post(
        "/movies/",
        json={
            "title": "Forrest Gump",
            "description": "A movie",
            "release_date": "1994-07-06",
        },
    )

    assert movie_response.status_code == 200
    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/actors/{actor_id}/movies/{movie_id}"
    )

    assert response.status_code == 200

    response = client.post(
        f"/actors/{actor_id}/movies/{movie_id}"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Movie already associated with this actor"
    )


def test_get_actor_movies(client):
    actor_response = client.post(
        "/actors/",
        json={
            "name": "Tom Hanks",
        },
    )

    assert actor_response.status_code == 200
    actor_id = actor_response.json()["actor_id"]

    movie_response = client.post(
        "/movies/",
        json={
            "title": "Forrest Gump",
            "description": "A movie",
            "release_date": "1994-07-06",
        },
    )

    assert movie_response.status_code == 200
    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/actors/{actor_id}/movies/{movie_id}"
    )

    assert response.status_code == 200

    response = client.get(
        f"/actors/{actor_id}/movies"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["movie_id"] == movie_id
    assert data[0]["title"] == "Forrest Gump"


def test_get_actor_movies_actor_not_found(client):
    response = client.get("/actors/9999/movies")

    assert response.status_code == 404
    assert response.json()["detail"] == "Actor not found"