import sqlalchemy.sql.expression


from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, Boolean)
from databases import Database
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True, index=True),
    Column('fullname', String(150)),
    Column('is_active', Boolean, server_default=sqlalchemy.true(), nullable=False),
    Column('hashed_password', String()),
)

database = Database(DATABASE_URI)
