from sqlalchemy.ext.asyncio import AsyncSession


class ProviderService:
    def __init__(self, session: AsyncSession):
        self.session = session
