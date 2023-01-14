from .users import users
from .posts import posts
from .reactions import reactions
from .base import metadata, engine

metadata.create_all(bind=engine)
