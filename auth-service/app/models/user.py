from app.db.database import metadata
from sqlalchemy import (Column, String,
                        Boolean, Table)
from sqlalchemy.dialects.postgresql import UUID

users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), unique=True, primary_key=True),
    Column('username', String(100), unique=True, index=True),
    Column('fullname', String(250)),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('is_premium', Boolean, default=False, nullable=False)
)
