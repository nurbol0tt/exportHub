from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URI = "postgresql+asyncpg://postgres:nur_2308@localhost:5432/export_hub_db"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
    JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"  # should be kept secret
    JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"
    ALGORITHM = "HS256"
    EXPIRE_MINUTES = 30


settings = Settings()