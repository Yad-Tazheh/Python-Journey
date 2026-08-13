
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