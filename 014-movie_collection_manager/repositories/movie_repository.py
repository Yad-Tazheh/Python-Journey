from ast import List

from sqlalchemy.orm import Session

from models import Movie, movie


class MovieRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Movie]:
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
        movie = self.get_by_id(movie_id)
        if movie:
            self.db.delete(movie)
            self.db.commit()
        return movie
