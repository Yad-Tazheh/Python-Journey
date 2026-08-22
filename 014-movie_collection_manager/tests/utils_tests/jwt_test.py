from utils.jwt import (
    create_access_token,
    decode_access_token,
)


def test_create_and_decode_access_token():
    token = create_access_token(
        {"sub": "1"}
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "1"
    assert "exp" in payload