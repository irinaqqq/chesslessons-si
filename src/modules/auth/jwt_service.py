import jwt
import uuid
from typing import Literal
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

from src.models import UserTable
from src.core.logger import logger

class JWTService:
    def __init__(self, algorithm: str, secret_key: str, access_expiry: int, refresh_expiry: int):
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_expiry_minutes = access_expiry
        self.refresh_expiry_minutes = refresh_expiry

    def generate_access_token(self, user: UserTable) -> str:
        return self.create_token(user, self.access_expiry_minutes, "access")


    def generate_refresh_token(self, user: UserTable) -> str:
        return self.create_token(user, self.refresh_expiry_minutes, "refresh")


    def create_token(
        self,
        user: UserTable,
        expires_minutes: int,
        token_type: Literal["access", "refresh", "recovery"]
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user.email,
            "id": str(user.id),
            "type": token_type,
            "jti": str(uuid.uuid4()),
            "iat": now,
            "exp": now + timedelta(minutes=expires_minutes),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)


    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise HTTPException(status_code=403, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            raise HTTPException(status_code=403, detail="Invalid token")
