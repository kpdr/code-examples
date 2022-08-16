import uuid

from environs import Env

env = Env()
env.read_env()
db_host = env.str("DB_HOST", default="127.0.0.1")

ENV = env.str("FLASK_ENV", default="development")
DEBUG = ENV == "development"

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://exampleuser:dev@{db_host}/example"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = env.str("SECRET_KEY", default=str(uuid.uuid4()))
