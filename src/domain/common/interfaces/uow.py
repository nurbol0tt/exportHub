from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


def get_session() -> AsyncSession:
    raise NotImplementedError


async def async_session_maker() -> sessionmaker:
    raise NotImplementedError