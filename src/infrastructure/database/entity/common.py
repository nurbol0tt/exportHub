import uuid

import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy import func
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    metadata: MetaData

    id = sa.Column(
        psql.UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True,
    )
    created_at = sa.Column(
        sa.DateTime,
        server_default=func.now()
    )
    updated_at = sa.Column(
        sa.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
