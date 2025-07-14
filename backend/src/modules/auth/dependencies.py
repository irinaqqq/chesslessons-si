from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from src.models import UserTable
from src.core.database import get_db
from src.core.dependencies import get_config
from src.modules.auth.service import AuthService
from src.modules.users.service import UserService
from src.modules.auth.jwt_service import JWTService
from src.modules.auth.password_manager import PasswordManager

token_scheme = HTTPBearer(auto_error=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_auth_service() -> AuthService:
    return AuthService(
        jwt_service=JWTService(
            algorithm=get_config().ALGORITHM,
            secret_key=get_config().SECRET_KEY,
            access_expiry=get_config().ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_expiry=get_config().REFRESH_TOKEN_EXPIRE_MINUTES,
        ),
        password_manager=PasswordManager(),
        user_service=UserService(),
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserTable:
    payload = auth_service.jwt_service.decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=403, detail="Invalid token type")
    return await auth_service.user_service.get_by_email(payload["sub"], db)


def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(token_scheme)) -> str:
    return credentials.credentials
