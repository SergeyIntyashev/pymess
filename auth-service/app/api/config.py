from os import environ
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = "HS256"
DATABASE_URI = environ.get('DATABASE_URI')

