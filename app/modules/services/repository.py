from sqlalchemy.ext.asyncio import AsyncSession


class ProviderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session