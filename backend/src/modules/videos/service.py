from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import VideoTable
from src.modules.videos.crud import VideoDatabase
from src.modules.videos.schemas import VideoCreate, VideoUpdate, VideoFilter


class VideoService:
    def __init__(self, database: VideoDatabase):
        self.database = database

    async def create_video(self, data: VideoCreate, db: AsyncSession) -> VideoTable:
        return await self.database.create(db, obj_in=data)

    async def update_video(self, video_id: UUID, data: VideoUpdate, db: AsyncSession) -> VideoTable:
        db_obj = await self.database.get(db, id=video_id)
        return await self.database.update(db, db_obj=db_obj, obj_in=data)

    async def get_by_id(self, video_id: UUID, db: AsyncSession) -> VideoTable:
        return await self.database.get(db, id=video_id)

    async def get_all(self, db: AsyncSession) -> List[VideoTable]:
        return await self.database.get_multi(db)

    async def get_available_for_user(
        self,
        user_id: UUID,
        db: AsyncSession,
        filters: VideoFilter | None = None
    ) -> List[VideoTable]:
        free_videos = await self.database.get_objects(db, return_many=True, access_level=0)
        purchased_ids = await self._get_user_purchased_video_ids(user_id, db)
        purchased_videos = await self.database.get_by_ids(db, ids=purchased_ids) if purchased_ids else []

        combined = {v.id: v for v in free_videos + purchased_videos}.values()

        if filters:
            if filters.access_level is not None:
                combined = [v for v in combined if v.access_level == filters.access_level]
            if filters.chess_level is not None:
                combined = [v for v in combined if v.level_required == filters.chess_level]

        return list(combined)

    async def _get_user_purchased_video_ids(self, user_id: UUID, db: AsyncSession) -> list[UUID]:
        # Заглушка — логика покупок будет позже
        return []
