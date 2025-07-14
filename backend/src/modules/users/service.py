from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .crud import UserDatabase
from src.models import UserTable

class UserService:
    def __init__(self, database: UserDatabase):
        self.database = database

    async def create_user(
        self,
        email: str,
        hashed_password: str,
        chess_level: str,
        db: AsyncSession
    ) -> UserTable:
        existing = await self.database.get_objects(db, email=email)
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        return await self.database.create(db, obj_in={
            "email": email,
            "hashed_password": hashed_password,
            "chess_level": chess_level
        })


    async def get_by_email(self, email: str, db: AsyncSession) -> UserTable:
        return await self.database.get_objects(db, email=email)


    async def get_by_id(self, user_id: UUID, db: AsyncSession) -> UserTable:
        return await self.database.get(db, id=user_id)


    async def update_user_password(self, user_id: UUID, hashed_password: str, db: AsyncSession) -> UserTable:
        user = await self.get_by_id(user_id, db)
        return await self.database.update(db, db_obj=user, obj_in={"hashed_password": hashed_password})