from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext


class HitFactorRequestContext(BaseContext):
    def __init__(self, db: AsyncSession):
        self.db = db
