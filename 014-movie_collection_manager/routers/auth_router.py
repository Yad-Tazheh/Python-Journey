from fastapi import APIRouter, Depends

from schemas.auth_schema import RegisterRequest
from schemas.user_schema import UserResponse
from services.auth_service import AuthService
from dependencies import get_auth_service, get_current_user, get_user_service, require_admin
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse)
def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.register(
        username=request.username,
        password=request.password,
    )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token = auth_service.login(
        username=form_data.username,
        password=form_data.password,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }





@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
        _: User = Depends(require_admin),
):
    return user_service.delete(user_id)