from .base import metadata

import sqlalchemy
import datetime

reactions = sqlalchemy.Table("reactions",
                             metadata,
                             sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True,
                                               unique=True),
                             sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                               nullable=False),
                             sqlalchemy.Column("post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id'),
                                               nullable=False),
                             sqlalchemy.Column("like", sqlalchemy.Boolean),
                             sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
                             sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
                             # sqlalchemy.Column("likes", sqlalchemy.String),
                             # sqlalchemy.Column("dislikes", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
                             )
