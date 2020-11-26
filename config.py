import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

db_path = os.environ.get("DATABASE_URL")
secret = os.environ.get("SECRET_KEY")


class Config:
    SECRET_KEY = secret
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
