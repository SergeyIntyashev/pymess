import databases
from sqlalchemy import create_engine, MetaData

from core.config import db_settings

database = databases.Database(db_settings.db_uri)

engine = create_engine(db_settings.db_uri)

metadata = MetaData()
