from dishka import Provider, provide

from src.domain.user.interfaces.persistence import IUserRepository, IUserReader
from src.infrastructure.database.repositories.user import UserRepository, UserReader


class RepositoryProvider(Provider):
    user_repository = provide(UserRepository, provides=IUserRepository)
    user_reader_repository = provide(UserReader, provides=IUserReader)
