from datetime import datetime

from sqlalchemy import (Column, String,
                        Boolean, Table, DateTime, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import true

from database import metadata

users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('username', String(100), unique=True, index=True),
    Column('fullname', String(250)),
    Column('is_active', Boolean, server_default=true, nullable=False),
    Column('hashed_password', String, nullable=False),
)

rooms = Table(
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('title', String(250), nullable=False),
    Column('admin', ForeignKey('users.id'), primary_key=True),
)

users_rooms = Table(
    'users_rooms',
    metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('room_id', ForeignKey('rooms.id', ondelete='CASCADE'), primary_key=True),
)

blocked_users = Table(
    'blocked_users',
    metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('owner_id', ForeignKey('users.id'), primary_key=True),
    Column('expiration_time', DateTime, default=datetime.max),
)

messages = Table(
    'messages',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('content', String, nullable=False),
    Column('create_at', DateTime, default=datetime.now),
    Column('update_at', DateTime, onupdate=datetime.now),
    Column('sender_id', UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column('recipient_id', UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
    Column('room_id', UUID(as_uuid=True), ForeignKey("rooms.id", ondelete='CASCADE'), nullable=False, index=True),
)
