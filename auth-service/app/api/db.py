import os
import sqlalchemy.sql.expression


from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, Boolean)
from databases import Database
from dotenv import load_dotenv

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()
load_dotenv()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True, index=True),
    Column('email', String(100)),
    Column('fullname', String(150)),
    Column('is_active', Boolean, server_default=sqlalchemy.true(), nullable=False),
    Column('hashed_password', String()),
)

database = Database(DATABASE_URI)
