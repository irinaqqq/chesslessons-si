from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.modules.users.service import UserService
from src.modules.auth.jwt_service import JWTService
from src.modules.auth.schemas import RegisterRequest
from src.modules.auth.password_manager import PasswordManager

class AuthService:
    def __init__(self, jwt_service: JWTService, password_manager: PasswordManager, user_service: UserService):
        self.jwt_service = jwt_service
        self.password_manager = password_manager
        self.user_service = user_service
        self.revoked_tokens: dict[str, int] = {}

    async def register_user(self, data: RegisterRequest, db: AsyncSession):
        hashed_password = self.password_manager.hash_password(data.password)
        await self.user_service.create_user(data.email, hashed_password, data.chess_level, db)
        return await self.authenticate_user(data.email, data.password, db)


    async def authenticate_user(self, email: str, password: str, db: AsyncSession):
        user = await self.user_service.get_by_email(email, db)
        if not self.password_manager.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        return (
            self.jwt_service.generate_access_token(user),
            self.jwt_service.generate_refresh_token(user)
        )


    async def refresh_token(self, token: str, db: AsyncSession):
        payload = self.jwt_service.decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=403, detail="Invalid token type")
        if jti := payload.get("jti"):
            if jti in self.revoked_tokens:
                raise HTTPException(status_code=403, detail="Refresh token is revoked")
        user = await self.user_service.get_by_email(payload["sub"], db)
        return self.jwt_service.generate_access_token(user)
    

    async def send_password_recovery_email(self, email: str, db: AsyncSession):
        user = await self.user_service.get_by_email(email, db)
        recovery_token = self.jwt_service.create_token(user, 30, "recovery")
        logger.info(f"[dev] Password recovery token for {email}: {recovery_token}")


    async def process_change_password(self, token: str, new_password: str, db: AsyncSession):
        payload = self.jwt_service.decode_token(token)
        if payload.get("type") != "recovery":
            raise HTTPException(status_code=403, detail="Invalid token type")
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token payload")
        hashed = self.password_manager.hash_password(new_password)
        user = await self.user_service.update_user_password(user_id, hashed, db)
        return await self.authenticate_user(user.email, new_password, db)


    async def logout_user(self, refresh_token: str):
        self._cleanup_revoked_tokens() 

        payload = self.jwt_service.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=403, detail="Invalid token type")

        jti = payload.get("jti")
        exp_timestamp = payload.get("exp")
        now_ts = int(datetime.now(timezone.utc).timestamp())

        if not jti or not exp_timestamp:
            raise HTTPException(status_code=403, detail="Invalid token payload")

        ttl = exp_timestamp - now_ts
        if ttl <= 0:
            logger.info(f"Refresh token already expired (jti={jti}), skipping revoke.")
            return

        self.revoked_tokens[jti] = exp_timestamp
        logger.info(f"Refresh token revoked: {jti} (TTL={ttl} seconds)")

    def _cleanup_revoked_tokens(self):
        now_ts = int(datetime.now(timezone.utc).timestamp())
        old_size = len(self.revoked_tokens)

        self.revoked_tokens = {
            jti: exp for jti, exp in self.revoked_tokens.items() if exp > now_ts
        }

        cleaned = old_size - len(self.revoked_tokens)
        if cleaned > 0:
            logger.info(f"Cleaned up {cleaned} expired revoked tokens")
