from sqlalchemy.orm import Session

from models import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Genre]:
        return self.db.query(Genre).all()

    def get_by_id(self, genre_id: int) -> Genre | None:
        return self.db.query(Genre).filter(Genre.genre_id == genre_id).first()

    def get_by_name(self, name: str) -> Genre | None:
        return self.db.query(Genre).filter(Genre.name == name).first()

    def create(self, genre: Genre) -> Genre:
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)

        return genre

    def update(self, genre: Genre) -> Genre:
        self.db.commit()
        self.db.refresh(genre)

        return genre

    def delete(self, genre_id: int) -> Genre | None:
        genre = self.get_by_id(genre_id)

        if genre:
            self.db.delete(genre)
            self.db.commit()

        return genre

