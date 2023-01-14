from .base import metadata

import sqlalchemy
import datetime


users = sqlalchemy.Table("users",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
                         sqlalchemy.Column("email", sqlalchemy.String, primary_key=True, unique=True),
                         sqlalchemy.Column("name", sqlalchemy.String),
                         sqlalchemy.Column("hashed_password", sqlalchemy.String),
                         )
