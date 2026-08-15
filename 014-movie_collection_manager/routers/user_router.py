from fastapi import APIRouter, Depends

from dependencies import get_user_service
from models.user import User
from schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_all()


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    new_user = User(
        username=user.username,
    )

    return user_service.create(new_user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = User(
        username=user.username,
    )

    return user_service.update(user_id, updated_user)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.delete(user_id)