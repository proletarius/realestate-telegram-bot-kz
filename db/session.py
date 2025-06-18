from sqlalchemy.ext.asyncio import AsyncSession
from db.database import AsyncSessionLocal

from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
