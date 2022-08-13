from datetime import datetime

import sqlalchemy.sql.expression

from uuid import uuid4

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database import Model


class Message(Model):
   __tablename__ = "messages"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
   content = Column(String)
   dispatch_time = Column(DateTime(), default=datetime.now)
   is_edited = Column(Boolean, server_default=sqlalchemy.false(), nullable=False)
#    sender = 
#    recipient =  