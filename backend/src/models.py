from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base

class ChessLevelEnum(str, Enum):
    BEGINNER = "Beginner"
    AMATEUR = "Amateur"
    CANDIDATE_MASTER = "Candidate Master"
    MASTER = "Master"


class AccessLevelEnum(int, Enum):
    FREE = 0
    ONE_TIME = 1
    SUBSCRIPTION = 2


class UserTable(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    chess_level = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CategoryTable(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class VideoTable(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    preview_url = Column(String)
    hls_url = Column(String)
    access_level = Column(Integer, default=0)  # FREE / ONE_TIME / SUBSCRIPTION
    level_required = Column(String)  # Beginner / Amateur / etc
    price = Column(Numeric, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PurchaseTable(Base):
    __tablename__ = "purchases"
    __table_args__ = (UniqueConstraint("user_id", "video_id", name="unique_purchase"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    purchase_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ViewLogTable(Base):
    __tablename__ = "views"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="SET NULL"))
    viewed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
