from sqlalchemy.ext.asyncio import AsyncSession


class PersonalRepo:
    def __init__(self, session: AsyncSession):
        self.session = session