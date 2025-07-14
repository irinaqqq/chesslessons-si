from .crud import UserDatabase
from .service import UserService

def get_user_service() -> UserService:
    return UserService(UserDatabase())