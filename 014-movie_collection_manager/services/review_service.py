from models import Review

from exceptions.movie_exceptions import MovieNotFoundException
from exceptions.review_exceptions import ReviewNotFoundException
from exceptions.user_exceptions import UserNotFoundException

from repositories.movie_repository import MovieRepository
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository


class ReviewService:
    def __init__(
        self,
        review_repository: ReviewRepository,
        user_repository: UserRepository,
        movie_repository: MovieRepository,
    ) -> None:
        self.review_repository = review_repository
        self.user_repository = user_repository
        self.movie_repository = movie_repository

    def get_all(self) -> list[Review]:
        return self.review_repository.get_all()

    def get_by_id(self, review_id: int) -> Review:
        review = self.review_repository.get_by_id(review_id)

        if not review:
            raise ReviewNotFoundException("Review not found")

        return review

    def get_by_user_id(self, user_id: int) -> list[Review]:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException("User not found")

        return self.review_repository.get_by_user_id(user_id)

    def get_by_movie_id(self, movie_id: int) -> list[Review]:
        movie = self.movie_repository.get_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        return self.review_repository.get_by_movie_id(movie_id)

    def create(self, review: Review) -> Review:
        user = self.user_repository.get_by_id(review.user_id)

        if not user:
            raise UserNotFoundException("User not found")

        movie = self.movie_repository.get_by_id(review.movie_id)

        if not movie:
            raise MovieNotFoundException("Movie not found")

        return self.review_repository.create(review)

    def update(
        self,
        review_id: int,
        updated_review: Review,
    ) -> Review:
        review = self.review_repository.get_by_id(review_id)

        if not review:
            raise ReviewNotFoundException("Review not found")

        review.content = updated_review.content
        review.rating = updated_review.rating

        return self.review_repository.update(review)

    def delete(self, review_id: int) -> Review:
        review = self.review_repository.get_by_id(review_id)

        if not review:
            raise ReviewNotFoundException("Review not found")

        self.review_repository.delete(review_id)

        return review