from fastapi import APIRouter

from src.presentation.handlers.user import user_router


def bind_routes():
    router = APIRouter(prefix='/api')
    router.include_router(user_router)

    return router
