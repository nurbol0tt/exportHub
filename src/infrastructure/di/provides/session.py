from typing import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide, from_context,
)
from dishka.integrations import fastapi
from sqlalchemy import (
    orm,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, AsyncEngine,
)


from src.config import settings
from src.domain.common.interfaces.uow import async_session_maker, get_session


class SessionProvider(Provider):
    request = from_context(provides=fastapi.Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(
            settings.POSTGRES_URI, pool_pre_ping=True, future=True,
        )

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine) -> async_session_maker:
        return orm.sessionmaker(
            engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(provides=get_session, scope=Scope.REQUEST)
    async def _get_session(self, session_maker: async_session_maker) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
