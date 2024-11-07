from dishka.integrations.starlette import setup_dishka
from fastapi import FastAPI

from src.infrastructure.di.container import get_container
from src.presentation.handlers.register import bind_routes


def initialize_app(_app: FastAPI) -> FastAPI:
    _app.include_router(bind_routes())
    # register_exceptions(_app)
    container = get_container()
    setup_dishka(container, _app)
    return _app


app = initialize_app(
    FastAPI(),
)

# python = "^3.10"
# fastapi = "^0.115.4"
# sqlalchemy = "^2.0.36"
# dishka = "^1.4.0"
# python-jose = "^3.3.0"
# passlib = "^1.7.4"
# alembic = "^1.14.0"
# asyncpg = "^0.30.0"
# psycopg2-binary = "^2.9.10"
# uvicorn = "^0.32.0"