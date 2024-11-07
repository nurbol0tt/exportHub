import sqlalchemy as sa

from src.infrastructure.database.entity.common import Base


class User(Base):
    __tablename__ = "users"

    username = sa.Column(
        sa.String,
        unique=True,
        nullable=False,
    )
    email = sa.Column(
        sa.String,
        unique=True,
        nullable=False,
    )
    password = sa.Column(
        sa.String(255),
        nullable=False,
    )



# class Profile(Base):
#     __tablename__ = "users"

    # user_id
    # phone =
    # company_name  =
    # company_description  =
