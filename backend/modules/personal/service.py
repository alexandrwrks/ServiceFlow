from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users
from modules.personal.repo import PersonalRepo
from modules.personal.schemas import ProfileResponse


class PersonalService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = PersonalRepo(session)

    async def get_personal_stat(self, user: Users) -> ProfileResponse:
        return ProfileResponse.model_validate(user)