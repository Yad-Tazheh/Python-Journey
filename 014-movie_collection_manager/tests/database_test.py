from sqlalchemy import text

from models.actor import Actor
from models.genre import Genre
from models.movie import Movie
from models.review import Review
from models.user import User


def test_db_connect(test_session):
    result = test_session.execute(text("SELECT 1"))
    assert result.scalar() == 1



def test_create_genre(test_session):
    genre = Genre(
        name="Action"
    )
    test_session.add(genre)
    test_session.commit()

    saved_genre = test_session.get(Genre, genre.genre_id)

    assert saved_genre.name == "Action"


def test_create_movie(test_session):
    movie = Movie(
        title = "Interstellar",
        description = "A team of explorers travel through a wormhole in space in an attempt to save humanity.",
        release_date = "2014-11-07"
    )
    test_session.add(movie)
    test_session.commit()

    saved_movie = test_session.get(Movie, movie.movie_id)
    assert saved_movie.title == "Interstellar"


def test_movie_genre_relationship(test_session):
    genre = Genre(
        name="Action"
    )
    movie = Movie(
        title = "Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    test_session.add(movie)
    test_session.add(genre)
    movie.genres.append(genre)

    test_session.commit()

    saved_movie = test_session.get(Movie, movie.movie_id)

    assert len(saved_movie.genres) == 1
    assert saved_movie.genres[0].name == "Action"


def test_movie_actor_relationship(test_session):
    actor = Actor(
        name="Leonardo DiCaprio"
    )

    movie = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    test_session.add(actor)
    test_session.add(movie)
    movie.actors.append(actor)
    test_session.commit()

    saved_movie = test_session.get(Movie, movie.movie_id)

    assert saved_movie.title == "Interstellar"
    assert saved_movie.actors[0].name == "Leonardo DiCaprio"


def test_user_movie_review_relationship(test_session):
    user = User(
        username= "Ali"
    )

    movie = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    review = Review(
        content= "Amazing movie",
        rating=5,
        user=user,
        movie=movie
    )

    test_session.add(review)
    test_session.commit()

    saved_review = test_session.get(Review, review.review_id)

    assert saved_review.user.username == "Ali"
    assert saved_review.content == "Amazing movie"
    assert saved_review.rating == 5
    assert saved_review.movie.title == "Interstellar"