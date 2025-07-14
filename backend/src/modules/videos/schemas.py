from pydantic import BaseModel, HttpUrl
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class VideoBase(BaseModel):
    title: str
    description: str
    preview_url: HttpUrl
    hls_url: HttpUrl
    access_level: int  # 0 / 1 / 2
    level_required: str
    price: Decimal | None = None
    category_id: UUID | None = None


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class VideoRead(VideoBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class VideoFilter(BaseModel):
    access_level: int | None = None
    chess_level: str | None = None