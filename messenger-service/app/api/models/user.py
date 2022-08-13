import sqlalchemy.sql.expression

from uuid import uuid4

from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ..database import Model


class User(Model):
   __tablename__ = "users"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
   username = Column(String, unique=True, index=True)
   fullname = Column(String)
   is_active = Column(Boolean, server_default=sqlalchemy.true(), nullable=False)
   hashed_password = Column(String)
