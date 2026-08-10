from sqlalchemy import text

from models.actor import Actor
from models.genre import Genre
from models.movie import Movie
from models.review import Review
from models.user import User
from repositories import movie_repository
from repositories.movie_repository import MovieRepository

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


def test_create_movie_via_repo(test_session):
    movie_repository = MovieRepository(test_session)

    movie = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    movie_repository.create(movie)

    saved_movie = movie_repository.get_by_id(movie.movie_id)

    assert saved_movie is not None
    assert saved_movie.title == "Interstellar"

def test_get_movie_by_id(test_session):
    movie = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    movie_repository = MovieRepository(test_session)
    movie_repository.create(movie)
    saved_movie = movie_repository.get_by_title(movie.title)

    assert saved_movie is not None
    assert saved_movie.title == "Interstellar"

def test_get_all_movies(test_session):
    movie_repository = MovieRepository(test_session)

    movie1 = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    movie2 = Movie(
        title="Batman",
        description="a dark movie",
        release_date = "2011-11-07"
    )

    movie3 = Movie(
        title="Superman",
        description="a fantasy movie",
        release_date = "2018-11-07"
    )

    movie_repository.create(movie1)
    movie_repository.create(movie2)
    movie_repository.create(movie3)

    saved_movies = movie_repository.get_all()

    titles=[movie.title for movie in saved_movies]
    assert "Superman" in titles
    assert "Batman" in titles
    assert "Interstellar" in titles

def test_update_movie(test_session):

    movie_repository = MovieRepository(test_session)
    movie = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )

    movie_repository.create(movie)

    movie.description = "a fantasy movie"

    movie_repository.update(movie)

    assert movie.description == "a fantasy movie"


def test_delete_movie(test_session):
    movie_repository = MovieRepository(test_session)
    movie = Movie(
        title="Interstellar",
        description="a good movie",
        release_date = "2014-11-07"
    )
    movie_repository.create(movie)
    movie_repository.delete(movie.movie_id)
    saved_movie = movie_repository.get_by_id(movie.movie_id)
    assert saved_movie is None




