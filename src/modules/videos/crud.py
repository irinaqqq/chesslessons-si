from src.models import VideoTable
from src.core.crudbase import CRUDBase
from src.modules.videos.schemas import VideoCreate, VideoUpdate


class VideoDatabase(CRUDBase[VideoTable, VideoUpdate, VideoCreate]):
    pass