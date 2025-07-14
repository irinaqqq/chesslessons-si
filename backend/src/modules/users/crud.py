from src.models import UserTable
from src.core.crudbase import CRUDBase
from src.modules.users.schemas import UserCreate, UserUpdate

class UserDatabase(CRUDBase[UserTable, UserCreate, UserUpdate]):
    pass