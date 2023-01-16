import datetime

from asyncpg import UniqueViolationError
from typing import List

from core.exceptions import UserNotFoundException, UserAlreadyExistsException
from models.user import User, UserIn
from .base import BaseRepository
from core.security import hash_password
from db.users import users


class UserRepository(BaseRepository):
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(offset).order_by(users.c.id)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, user_id: int) -> User:
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query=query)
        if not user:
            raise UserNotFoundException
        return User.parse_obj(user)

    async def get_by_email(self, user_email: str) -> User:
        query = users.select().where(users.c.email == user_email)
        user = await self.database.fetch_one(query=query)
        if not user:
            raise UserNotFoundException
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        user = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**user.dict(exclude_unset=True)}

        query = users.insert().values(**values)
        try:
            user.id = await self.database.execute(query)
        except UniqueViolationError:
            raise UserAlreadyExistsException
        return user

    async def update(self, user_id: int, u: UserIn) -> User:
        user = User(
            id=user_id,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**user.dict(exclude_unset=True)}

        # something is not clear, looks like a hack
        # a better idea is to use raw connection to check updated count, but I don't wanna
        query = users.update().where(users.c.id == user_id).values(**values).returning(users.c.created_at)
        user_created_at_res = await self.database.execute(query)
        if not user_created_at_res:  # means if UPDATE returned nothing with RETURNING in statement
            raise UserNotFoundException

        user.created_at = user_created_at_res
        return user
