from datetime import datetime

from app.db.database import metadata
from sqlalchemy import (Column, String,
                        Table, DateTime, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID

rooms = Table(
    'rooms',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('title', String(250), nullable=False),
    Column('admin', ForeignKey('users.id'), primary_key=True),
)

users_rooms = Table(
    'users_rooms',
    metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('room_id', ForeignKey('rooms.id', ondelete='CASCADE'),
           primary_key=True),
)

blocked_users = Table(
    'blocked_users',
    metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('owner_id', ForeignKey('users.id'), primary_key=True),
    Column('expiration_time', DateTime, default=datetime.max),
)
