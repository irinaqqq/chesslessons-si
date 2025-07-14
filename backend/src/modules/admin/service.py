from sqlalchemy.ext.asyncio import AsyncSession

from src.services.redis.service import RedisService
from src.modules.leads.service import LeadsService
from src.modules.company.service import CompanyService
from src.modules.assistant.service import AssistantService
from src.modules.platform_user.service import PlatformUserService
from src.models import LeadsTable, PlatformUsersTable, AssistantTable, CompanyTable

class AdminService:
    def __init__(
        self, 
        leads_service = LeadsService,
        redis_service = RedisService,
        company_service = CompanyService,
        assistant_service = AssistantService,
        platform_user_service = PlatformUserService,
        ):
        self.leads_service = leads_service
        self.redis_service = redis_service
        self.company_service = company_service
        self.assistant_service = assistant_service
        self.platform_user_service = platform_user_service

    async def get_companies(self, db: AsyncSession, skip: int, limit: int) -> tuple[list[CompanyTable], int]:
        return await self.company_service.get_many(db, skip, limit)


    async def get_referrals(self, company_id: int, db: AsyncSession) -> list[CompanyTable]:
        return await self.company_service.get_referrals(company_id, db)


    async def get_leads_by_company_id(self, company_id: int, db: AsyncSession, skip: int, limit: int) -> tuple[list[LeadsTable], int]:
        return await self.leads_service.get_leads_by_company_id(company_id, db, skip, limit)
    

    async def delete_company(self, company_id: int, db: AsyncSession):
        await self.company_service.delete_company(company_id, db)


    async def get_platform_users(self, db: AsyncSession, skip: int, limit: int) -> tuple[list[PlatformUsersTable], int]:
        return await self.platform_user_service.get_platform_users(db, skip, limit)


    async def delete_platform_user(self, user_id: int, db: AsyncSession):
        await self.platform_user_service.delete_platform_user(user_id, db)


    async def get_assistants(self, db: AsyncSession, skip: int, limit: int) -> tuple[list[AssistantTable], int]:
        return await self.assistant_service.get_many(db, skip, limit)


    async def update_messages_number(self, assistant_id: str, messages_number: int, db: AsyncSession):
        await self.assistant_service.update_messages_number(assistant_id, messages_number, db)


    async def delete_thread_assistant(self, assistant_id: str, db: AsyncSession):
        await self.assistant_service.delete_thread_assistant(assistant_id, db)


    async def delete_thread_client(self, assistant_id: str, client_id: str, db: AsyncSession):
        await self.assistant_service.delete_thread_client(assistant_id, client_id, db)


    async def block_bot_fully(self, assistant_id: str):
        await self.redis_service.block_bot_fully(assistant_id)


    async def unblock_bot_fully(self, assistant_id: str):
        await self.redis_service.unblock_bot_fully(assistant_id)