

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