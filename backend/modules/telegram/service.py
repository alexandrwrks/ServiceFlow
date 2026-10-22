from sqlalchemy.ext.asyncio import AsyncSession

from modules.telegram.repo import TelegramRepo


class TelegramService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = TelegramRepo(session)