from sqlalchemy.orm import Session

from models.review import Review

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Review]:
        return self.db.query(Review).all()

    def get_by_id(self, review_id: int) -> Review | None:
        return self.db.query(Review).filter(Review.review_id == review_id).first()

    def get_by_user_id(self, user_id: int) -> list[Review]:
        return self.db.query(Review).filter(Review.user_id == user_id).all()

    def get_by_movie_id(self, movie_id: int) -> list[Review]:
        return self.db.query(Review).filter(Review.movie_id == movie_id).all()

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review

    def update(self, review: Review) -> Review:
        self.db.commit()
        self.db.refresh(review)

        return review

    def delete(self, review_id: int) -> Review | None:
        review = self.get_by_id(review_id)

        if review:
            self.db.delete(review)
            self.db.commit()

        return review