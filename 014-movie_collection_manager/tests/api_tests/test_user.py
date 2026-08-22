def test_get_all_users(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client, user_payload):
    response = client.post(
        "/users/",
        json=user_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "Test"


def test_get_user_by_id(client, created_user):
    user_id = created_user["user_id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["username"] == "Test"


def test_get_user_by_id_not_found(client):
    response = client.get("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user(client, created_user):
    user_id = created_user["user_id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "username": "Mike",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["username"] == "Mike"


def test_update_user_not_found(client):
    response = client.put(
        "/users/9999",
        json={
            "username": "Mike",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user(client, created_user):
    user_id = created_user["user_id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["username"] == "Test"

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_not_found(client):
    response = client.delete("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"