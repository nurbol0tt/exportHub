from typing import List, Protocol
from uuid import UUID

from src.infrastructure.database.entity.user import User


class IUserReader(Protocol):
    async def all_users(self) -> List[User]:
        ...

    async def user_by_id(self, user_id: UUID) -> User:
        ...

    async def get_user_by_email(self, email: str) -> User:
        ...

class IUserRepository(Protocol):
    async def insert_user(self, user: User) -> User:
        ...

    async def edit_user(self, user: User) -> User:
        ...
