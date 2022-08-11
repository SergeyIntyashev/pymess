import databases
from sqlalchemy import create_engine, MetaData

from ..core.config import get_db_settings

settings = get_db_settings()

database = databases.Database(settings.db_uri)

engine = create_engine(settings.db_uri)

metadata = MetaData()
