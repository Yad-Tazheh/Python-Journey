from sqlalchemy import text

from models.genre import Genre


def test_db_connect(test_session):
    result = test_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_create_genre(test_session):

    genre = Genre(
        name = "Action"
    )
    test_session.add(genre)
    test_session.commit()

    saved_genre = test_session.get(Genre, genre.genre_id)

    assert saved_genre.name == "Action"