from fastapi import Depends, HTTPException, status

from models.user import User
from core.security import JWTBearer, decode_access_token
from repositories.users import UserRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)


async def get_current_user(
    users: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer()),
) -> User:
    ex = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")

    payload = decode_access_token(token)
    if payload is None:
        raise ex

    email: str = payload.get("sub", None)
    if email is None:
        raise ex

    user = await users.get_by_email(email)
    if user is None:
        raise ex

    return user
