from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import (
    APIRouter,
)
from sqlalchemy.util import await_only

from src.domain.user.usecase.user import CreateUserService, AuthorizationService, UserProfileService
from src.presentation.handlers.requests.user import UserRegisterRequest, UserLoginRequest, TokenRequest

user_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    route_class=DishkaRoute
)


@user_router.post("/register")
async def create_user(dto: UserRegisterRequest, service: FromDishka[CreateUserService]):
    return await service(user=dto)


@user_router.post("/login")
async def login(dto: UserLoginRequest, service: FromDishka[AuthorizationService]):
    return await service(dto=dto)


@user_router.post("/refresh_token")
async def refresh_token():
    ...


@user_router.get("/profile/{token}")
async def profile(token: str, service: FromDishka[UserProfileService]):
    return await service(token=token)


@user_router.delete("/reset-password")
async def delete_products():
    ...
