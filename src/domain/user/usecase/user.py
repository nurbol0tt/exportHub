from datetime import datetime, timedelta
from typing import Final, Union, Any
from uuid import UUID

from jose import jwt, JWTError
from jose.exceptions import JWTClaimsError, ExpiredSignatureError
from passlib.context import CryptContext

from src.config import settings
from src.domain.common.interfaces.uow import get_session
from src.domain.user.interfaces.persistence import IUserRepository, IUserReader
from src.infrastructure.database.entity.user import User
from src.presentation.handlers.requests.user import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenRequest,
    UserProfileResponse,
)

pwd_context: Final = CryptContext(
    schemes=['bcrypt'], deprecated='auto',
)

class CreateUserService:
    def __init__(
            self,
            session: get_session,
            repo: IUserRepository,
    ):
        self._session = session
        self._repo = repo


    async def __call__(self, user: UserRegisterRequest):
        hashed_password = await self.hashing_secret(user.password)
        user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        await self._repo.insert_user(user)
        await self._session.commit()
        return {'message': 'User created successfully', 'username': user.username}

    @classmethod
    async def hashing_secret(cls, secret: str):
        return pwd_context.hash(secret=secret)


class AuthorizationService:

    def __init__(
            self,
            session: get_session,
            repo: IUserRepository,
            repo_reader: IUserReader,
    ) -> None:
        self.repo = repo
        self.session = session
        self.repo_reader = repo_reader

    async def authenticate_user(self, email: str, password: str) -> None | User:
        user = await self.repo_reader.get_user_by_email(email)  # Add await here

        if user and await self.verify_password(password, user.password):
            return user

    async def __call__(self, dto: UserLoginRequest):
        user = await self.authenticate_user(email=dto.email, password=dto.password)  # Add await here
        if not user:
            raise
            # raise AuthenticationError("Invalid email or password")

        access_token = await self.create_jwt_token(user_id=user.id, scopes=None)
        refresh_token = await self.create_refresh_token(subject=str(user.id))
        return {"access_token": access_token, "refresh_token": refresh_token}

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def create_jwt_token(cls, user_id: UUID, scopes: list | None):
        claims = dict(
            sub=user_id.__str__(),
            scopes=scopes,
            exp=datetime.utcnow() + timedelta(minutes=settings.EXPIRE_MINUTES)
        )
        return jwt.encode(
            claims=claims, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
        )


    @classmethod
    async def create_refresh_token(cls, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)

        return encoded_jwt


class UserProfileService:

    def __init__(
            self,
            repo: IUserReader,
            session: get_session,
    ) -> None:
        self.repo = repo
        self.session = session

    async def __call__(self, token: str):
        user_id = await self.decode_jwt_token(token)
        user = await self.repo.user_by_id(user_id=user_id)
        return UserProfileResponse(username=user.username, email=user.email).dict()

    async def decode_jwt_token(self, jwt_token: str) -> dict:
        try:
            payload = jwt.decode(
                jwt_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            if user_id is None:
                raise ValueError('Invalid token')

        except (JWTError, JWTClaimsError, ExpiredSignatureError) as e:
            raise ValueError(e)

        return user_id

