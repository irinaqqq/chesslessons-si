from .service import AdminService
from src.modules.leads.dependencies import get_leads_service
from src.services.redis.dependencies import get_redis_service
from src.modules.company.dependencies import get_company_service
from src.modules.assistant.dependencies import get_assistant_service
from src.modules.platform_user.dependencies import get_platform_user_service

def get_admin_service() -> AdminService:
    return AdminService(
        leads_service=get_leads_service(),
        redis_service=get_redis_service(),
        company_service=get_company_service(),
        assistant_service=get_assistant_service(),
        platform_user_service=get_platform_user_service(),
    )
