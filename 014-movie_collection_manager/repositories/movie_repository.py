
from sqlalchemy.orm import Session

from models import Movie


class MovieRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Movie]:
        return self.db.query(Movie).all()

    def get_by_id(self, movie_id: int) -> Movie | None:
        return (self.db.query(Movie).filter(Movie.movie_id == movie_id).first())

    def get_by_title(self, title: str) -> Movie | None:
        return (self.db.query(Movie).filter(Movie.title == title).first())


    def create(self, movie: Movie) -> Movie:
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie: Movie) -> Movie:
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie_id: int) -> Movie | None:
        existing_movie = self.get_by_id(movie_id)
        if existing_movie:
            self.db.delete(existing_movie)
            self.db.commit()
        return existing_movie
