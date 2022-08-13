from sqlalchemy import (Column, String,
                        Boolean, Table)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression

from app.db.database import metadata

users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('username', String(100), unique=True, index=True),
    Column('fullname', String(250)),
    Column('is_active', Boolean, server_default=expression.true(), nullable=False),
    Column('hashed_password', String),
)
