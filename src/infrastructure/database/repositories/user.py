from uuid import UUID

from sqlalchemy import select

from src.domain.user.interfaces.persistence import IUserRepository, IUserReader
from src.infrastructure.database.entity.user import User
from src.infrastructure.database.repositories.common import SQLAlchemyRepo


class UserRepository(SQLAlchemyRepo, IUserRepository):
    async def insert_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()

        return user

class UserReader(SQLAlchemyRepo, IUserReader):
    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def user_by_id(self, user_id: UUID) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
