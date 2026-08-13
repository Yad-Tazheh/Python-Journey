from fastapi import APIRouter, Depends

from dependencies import get_review_service
from schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewResponse
from services.review_service import ReviewService
from models.review import Review


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)

@router.get("/", response_model=list[ReviewResponse])
def get_all_reviews(
    review_service : ReviewService = Depends(get_review_service)
):
    return review_service.get_all()

@router.post("/", response_model=ReviewResponse)
def create_review(
    review : ReviewCreate,
    review_service : ReviewService = Depends(get_review_service)
):
    new_review = Review(
        content=review.content,
        rating=review.rating,
        user_id=review.user_id,
        movie_id=review.movie_id,
    )

    return review_service.create(new_review)

''''
Request Body
    │
    ├── content
    ├── rating
    ├── user_id
    └── movie_id
          │
          ▼
     ReviewCreate
          │
          ▼
   SQLAlchemy Review
    │       │       │
    │       │       └── movie_id
    │       └────────── user_id
    └────────────────── content/rating
          │
          ▼
    ReviewService
          │
     ┌────┴────┐
     ▼         ▼
   User      Movie
   Repo       Repo
     │         │
     └────┬────┘
          ▼
   ReviewRepository
'''

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review_by_id(
        review_id : int ,
        review_service : ReviewService = Depends(get_review_service)
):
    return review_service.get_by_id(review_id)

@router.get("/user/{user_id}", response_model=list[ReviewResponse])
def get_reviews_by_user(
        user_id : int ,
        review_service : ReviewService = Depends(get_review_service)
):
    return review_service.get_by_user_id(user_id)

@router.get("/movie/{movie_id}", response_model=list[ReviewResponse])
def get_reviews_by_movie(
        movie_id : int ,
        review_service : ReviewService = Depends(get_review_service)
):
    return review_service.get_by_movie_id(movie_id)

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
        review_id : int ,
        review: ReviewUpdate,
        review_service : ReviewService = Depends(get_review_service)
):
    updated_review = Review(
        content=review.content,
        rating=review.rating,
    )

    return review_service.update(review_id, updated_review)

@router.delete("/{review_id}", response_model=ReviewResponse)
def delete_review(
        review_id : int ,
        review_service : ReviewService = Depends(get_review_service)
):
    return review_service.delete(review_id)