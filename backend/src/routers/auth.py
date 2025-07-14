from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database import get_db
from src.schemas import StatusResponse
from src.modules.auth.service import AuthService
from src.modules.auth.dependencies import get_auth_service, get_bearer_token
from src.modules.auth.schemas import (
    TokenResponse,
    RegisterRequest,
    ChangePasswordRequest,
    ChangePassword
)

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/register", response_model=TokenResponse, summary="Register a new user")
async def register_user_route(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token = await auth_service.register_user(data, db)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse, summary="User login")
async def login_user_route(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token = await auth_service.authenticate_user(data.username, data.password, db)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/token/refresh", response_model=TokenResponse, summary="Refresh access token")
async def refresh_token_route(
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token = await auth_service.refresh_token(refresh_token, db)
    return TokenResponse(access_token=access_token)


@router.post("/password/recovery", response_model=StatusResponse, summary="Request password recovery email")
async def request_password_recovery_route(
    data: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.send_password_recovery_email(data.email, db)
    return StatusResponse(message="Recovery email sent")


@router.post("/password/reset", response_model=TokenResponse, summary="Reset password with recovery token")
async def reset_password_route(
    data: ChangePassword,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token = await auth_service.process_change_password(data.token, data.password, db)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", response_model=StatusResponse, summary="Logout user")
async def logout_user_route(
    refresh_token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout_user(refresh_token)
    return StatusResponse(message="Logged out successfully")