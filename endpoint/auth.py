from fastapi import APIRouter, Depends, HTTPException, status

from core.exceptions import UserNotFoundException
from models.token import Token, Login
from repositories.users import UserRepository
from core.security import verify_password, create_access_token

from .depends import get_user_repository


router = APIRouter()


@router.post("/", response_model=Token)
async def auth(login: Login, users: UserRepository = Depends(get_user_repository)):
    ex = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    try:
        user = await users.get_by_email(login.email)
        if not verify_password(login.password, user.hashed_password):
            raise ex
    except UserNotFoundException:
        raise ex

    return Token(
        access_token=create_access_token({"sub": login.email}),
        token_type="Bearer"
    )
