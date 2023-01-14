from starlette.config import Config

config = Config('.env')
DATABASE_URL = config("PG_DATABASE_URL", cast=str, default="")  # todo: rename variable
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = config("S_POSTING_SECRET_KEY", cast=str, default="2ecc8d1a9d5882f12a3acb3c7f05cff2")
