import datetime

from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from typing import List, Optional

from models.user import User, UserIn
from .base import BaseRepository
from core.security import hash_password
from db.users import users


class UserRepository(BaseRepository):
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(offset)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query=query)
        if not user:
            return None
        return User.parse_obj(user)

    async def get_by_email(self, user_email: str) -> User:
        query = users.select().where(users.c.email == user_email)
        user = await self.database.fetch_one(query=query)
        if not user:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        user = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**user.dict()}
        values.pop('id', None)  # autoincrement, omitting from INSERT query

        query = users.insert().values(**values)
        try:
            user.id = await self.database.execute(query)
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Account already registered with this email address"
            )
        return user

    async def update(self, user_id: int, u: UserIn) -> Optional[User]:
        user = User(
            id=user_id,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**user.dict()}
        values.pop('created_at', None)  # data that must not to be updated
        values.pop('id', None)

        # todo: mb need some changes
        query = users.update().where(users.c.id == user_id).values(**values).returning(users.c.created_at)
        user_created_at_res = await self.database.execute(query)
        if user_created_at_res:
            user.created_at = user_created_at_res
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{user.id}' was not found")
