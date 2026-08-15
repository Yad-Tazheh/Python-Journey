from models import Movie

from repositories.actor_repository import ActorRepository
from repositories.genre_repository import GenreRepository
from repositories.movie_repository import MovieRepository

from exceptions.actor_exceptions import (
    ActorAlreadyAssociatedException,
    ActorNotFoundException,
)
from exceptions.genre_exceptions import (
    GenreAlreadyAssociatedException,
    GenreNotFoundException,
)
from exceptions.movie_exceptions import (
    MovieAlreadyExistsException,
    MovieNotFoundException,
)


class MovieService:
    def __init__(
        self,
        movie_repository: MovieRepository,
        actor_repository: ActorRepository,
        genre_repository: GenreRepository,
    ) -> None:
        self.movie_repository = movie_repository
        self.actor_repository = actor_repository
        self.genre_repository = genre_repository

    def get_all(self) -> list[Movie]:
        return self.movie_repository.get_all()

    def get_by_id(self, movie_id: int) -> Movie:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        return movie

    def get_by_title(self, title: str) -> Movie:
        movie = self.movie_repository.get_by_title(title)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        return movie

    def create(self, movie: Movie) -> Movie:
        existing_movie = self.movie_repository.get_by_title(movie.title)

        if existing_movie:
            raise MovieAlreadyExistsException("Movie already exists")

        return self.movie_repository.create(movie)

    def update(
        self,
        movie_id: int,
        updated_movie: Movie,
    ) -> Movie:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        movie.title = updated_movie.title
        movie.description = updated_movie.description
        movie.release_date = updated_movie.release_date

        return self.movie_repository.update(movie)

    def delete(self, movie_id: int) -> Movie:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        self.movie_repository.delete(movie_id)

        return movie

    def add_actor(
        self,
        movie_id: int,
        actor_id: int,
    ) -> Movie:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        actor = self.actor_repository.get_by_id(actor_id)

        if not actor:
            raise ActorNotFoundException("Actor not found")

        if actor in movie.actors:
            raise ActorAlreadyAssociatedException(
                "Actor already associated with the movie"
            )

        movie.actors.append(actor)

        return self.movie_repository.update(movie)

    def get_actors(self, movie_id: int) -> list:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        return movie.actors

    def add_genre(
        self,
        movie_id: int,
        genre_id: int,
    ) -> Movie:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        genre = self.genre_repository.get_by_id(genre_id)

        if not genre:
            raise GenreNotFoundException("Genre not found")

        if genre in movie.genres:
            raise GenreAlreadyAssociatedException(
                "Genre already associated with the movie"
            )

        movie.genres.append(genre)

        return self.movie_repository.update(movie)

    def get_genres(self, movie_id: int) -> list:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        return movie.genres