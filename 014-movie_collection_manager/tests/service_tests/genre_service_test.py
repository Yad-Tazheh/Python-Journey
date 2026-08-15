from models import Genre, Movie

from exceptions.genre_exceptions import (
    GenreAlreadyExistsException,
    GenreAlreadyAssociatedException,
    GenreNotFoundException,
)
from exceptions.movie_exceptions import MovieNotFoundException

from repositories.genre_repository import GenreRepository
from repositories.movie_repository import MovieRepository


class GenreService:
    def __init__(
        self,
        genre_repository: GenreRepository,
        movie_repository: MovieRepository,
    ) -> None:
        self.genre_repository = genre_repository
        self.movie_repository = movie_repository

    def get_all(self) -> list[Genre]:
        return self.genre_repository.get_all()

    def get_by_id(self, genre_id: int) -> Genre:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        return existing_genre

    def get_by_name(self, genre_name: str) -> Genre:
        existing_genre = self.genre_repository.get_by_name(genre_name)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        return existing_genre

    def create(self, genre: Genre) -> Genre:
        existing_genre = self.genre_repository.get_by_name(genre.name)

        if existing_genre:
            raise GenreAlreadyExistsException("Genre already exists")

        return self.genre_repository.create(genre)

    def update(self, genre_id: int, updated_genre: Genre) -> Genre:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        existing_genre.name = updated_genre.name

        return self.genre_repository.update(existing_genre)

    def delete(self, genre_id: int) -> Genre:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        self.genre_repository.delete(genre_id)

        return existing_genre

    def add_movie(self, genre_id: int, movie_id: int) -> Genre:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        existing_movie = self.movie_repository.get_by_id(movie_id)

        if not existing_movie:
            raise MovieNotFoundException("Movie not found")

        if existing_movie in existing_genre.movies:
            raise GenreAlreadyAssociatedException(
                "Movie already associated with this genre"
            )

        existing_genre.movies.append(existing_movie)

        return self.genre_repository.update(existing_genre)

    def get_movies(self, genre_id: int) -> list[Movie]:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        return existing_genre.movies