from models import Movie
from repositories.movie_repository import MovieRepository
from exceptions.movie_exceptions import MovieAlreadyExistsException, MovieNotFoundException

class MovieService:
    def __init__(self, movie_repository: MovieRepository) -> None:
        self.movie_repository = movie_repository

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