from models import Genre

from repositories.genre_repository import GenreRepository
from exceptions.genre_exceptions import GenreNotFoundException, GenreNotFoundException, GenreAlreadyExistsException


class GenreService:
    def __init__(self, genre_repository: GenreRepository) -> None:
        self.genre_repository = genre_repository


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


    def update(self, genre_id: int, update_genre: Genre) -> Genre:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        existing_genre.name = update_genre.name

        return self.genre_repository.update(existing_genre)

    def delete(self, genre_id: int) -> Genre:
        existing_genre = self.genre_repository.get_by_id(genre_id)

        if not existing_genre:
            raise GenreNotFoundException("Genre not found")

        self.genre_repository.delete(genre_id)

        return existing_genre


