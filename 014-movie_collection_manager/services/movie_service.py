from models import Movie
from repositories import actor_repository
from repositories.movie_repository import MovieRepository
from repositories.actor_repository import ActorRepository
from repositories.genre_repository import GenreRepository

from exceptions.movie_exceptions import MovieAlreadyExistsException, MovieNotFoundException
from exceptions.actor_exceptions import ActorNotFoundException, ActorAlreadyAssociatedException
from exceptions.genre_exceptions import GenreNotFoundException, GenreAlreadyAssociatedException


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

    def get_by_id(self, movie_id: int) -> Movie:
        existing_movie = self.movie_repository.get_by_id(movie_id)
        if not existing_movie:
            raise MovieNotFoundException('Movie not found')
        return existing_movie

    def get_all(self) -> list[Movie]:
        return self.movie_repository.get_all()

    def get_by_title(self, title: str) -> Movie:
        existing_movie = self.movie_repository.get_by_title(title)
        if not existing_movie:
            raise MovieNotFoundException('Movie not found')
        return existing_movie


    def create(self, movie: Movie) -> Movie:
        existing_movie = self.movie_repository.get_by_title(movie.title)

        if existing_movie:
            raise MovieAlreadyExistsException('Movie already exists')

        return self.movie_repository.create(movie)

    def update(self, movie_id: int, updated_movie: Movie) -> Movie:
        existing_movie = self.movie_repository.get_by_id(movie_id)

        if not existing_movie:
            raise MovieNotFoundException('Movie not found')

        existing_movie.title = updated_movie.title
        existing_movie.description = updated_movie.description
        existing_movie.release_date = updated_movie.release_date

        return self.movie_repository.update(existing_movie)

    def delete(self, movie_id: int) -> Movie:
        existing_movie = self.movie_repository.get_by_id(movie_id)

        if not existing_movie:
            raise MovieNotFoundException('Movie not found')
        self.movie_repository.delete(movie_id)

        return existing_movie


    def add_actor(self, movie_id: int, actor_id: int) -> Movie:
        existing_movie = self.movie_repository.get_by_id(movie_id)
        if not existing_movie:
            raise MovieNotFoundException('Movie not found')

        existing_actor = self.actor_repository.get_by_id(actor_id)
        if not existing_actor:
            raise ActorNotFoundException('Actor not found')

        if existing_actor in existing_movie.actors:
            raise ActorAlreadyAssociatedException('Actor already associated with the movie')

        existing_movie.actors.append(existing_actor)
        self.movie_repository.update(existing_movie)

        return existing_movie


    def get_actors(self, movie_id: int) -> list:
        existing_movie = self.movie_repository.get_by_id(movie_id)
        if not existing_movie:
            raise MovieNotFoundException('Movie not found')

        return existing_movie.actors


    def get_genres(self, movie_id: int) -> list:
        existing_movie = self.movie_repository.get_by_id(movie_id)
        if not existing_movie:
            raise MovieNotFoundException('Movie not found')

        return existing_movie.genres


    def add_genre(self, movie_id: int, genre_id: int) -> Movie:
        existing_movie = self.movie_repository.get_by_id(movie_id)
        if not existing_movie:
            raise MovieNotFoundException('Movie not found')

        existing_genre = self.genre_repository.get_by_id(genre_id)
        if not existing_genre:
            raise GenreNotFoundException('Genre not found')

        if existing_genre in existing_movie.genres:
            raise GenreAlreadyAssociatedException('Genre already associated with the movie')

        existing_movie.genres.append(existing_genre)
        self.movie_repository.update(existing_movie)

        return existing_movie

