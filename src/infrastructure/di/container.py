from dishka import AsyncContainer, Scope, make_async_container

from src.infrastructure.di.provides.repositories import RepositoryProvider
from src.infrastructure.di.provides.services import ServiceProvider
from src.infrastructure.di.provides.session import SessionProvider



def get_container() -> AsyncContainer:
    repository_provider = RepositoryProvider(scope=Scope.REQUEST)
    service_provider = ServiceProvider(scope=Scope.REQUEST)
    session_provider = SessionProvider(scope=Scope.SESSION)

    return make_async_container(
        service_provider,
        repository_provider,
        session_provider,
    )