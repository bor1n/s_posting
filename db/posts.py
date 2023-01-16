from .base import metadata

import sqlalchemy
import datetime


posts = sqlalchemy.Table("posts",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
                         sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
                         sqlalchemy.Column("content", sqlalchemy.String),
                         sqlalchemy.Column("visibility", sqlalchemy.Integer),
                         sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
                         sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
                         )
