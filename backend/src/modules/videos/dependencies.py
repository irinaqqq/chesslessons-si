from .crud import VideoDatabase
from .service import VideoService


def get_video_service() -> VideoService:
    return VideoService(VideoDatabase())