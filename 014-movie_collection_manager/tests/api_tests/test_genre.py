

def test_get_all_genres(client):
    response = client.get("/genres/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_genre(client):
    response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Action"


def test_get_genre_by_id(client):
    response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert response.status_code == 200

    genre_id = response.json()["genre_id"]

    response = client.get(f"/genres/{genre_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["genre_id"] == genre_id
    assert data["name"] == "Action"


def test_get_genre_by_id_not_found(client):
    response = client.get("/genres/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Genre not found"


def test_update_genre(client):
    response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert response.status_code == 200

    genre_id = response.json()["genre_id"]

    response = client.put(
        f"/genres/{genre_id}",
        json={
            "name": "Comedy",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["genre_id"] == genre_id
    assert data["name"] == "Comedy"


def test_update_genre_not_found(client):
    response = client.put(
        "/genres/9999",
        json={
            "name": "Comedy",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Genre not found"


def test_delete_genre(client):
    response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert response.status_code == 200

    genre_id = response.json()["genre_id"]

    response = client.delete(f"/genres/{genre_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["genre_id"] == genre_id
    assert data["name"] == "Action"

    # Verify deletion
    response = client.get(f"/genres/{genre_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Genre not found"


def test_delete_genre_not_found(client):
    response = client.delete("/genres/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Genre not found"


def test_get_genre_by_name(client):
    response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert response.status_code == 200

    response = client.get("/genres/name/Action")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Action"


def test_get_genre_by_name_not_found(client):
    response = client.get("/genres/name/Unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Genre not found"


def test_add_movie_to_genre(client):
    genre_response = client.post(
        "/genres/",
        json={
            "name": "Action",
        },
    )

    assert genre_response.status_code == 200
    genre_id = genre_response.json()["genre_id"]

    movie_response = client.post(
        "/movies/",
        json={
            "title": "The Avengers",
            "description": "A superhero movie",
            "release_date": "2012-05-04",
        },
    )

    assert movie_response.status_code == 200
    movie_id = movie_response.json()["movie_id"]

    response = client.post(
        f"/genres/{genre_id}/movies/{movie_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["genre_id"] == genre_id
    assert data["name"] == "Action"