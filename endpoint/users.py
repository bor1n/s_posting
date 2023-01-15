from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.exceptions import UserNotFoundException, UserAlreadyExistsException
from models.user import User, UserIn
from repositories.users import UserRepository
from .depends import get_user_repository, get_current_user


router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        offset: int = 0,
):
    users = await users.get_all(limit=limit, offset=offset)
    return users


@router.post("/", response_model=User, response_model_exclude={"hashed_password"})
async def create_user(
        user: UserIn,
        users: UserRepository = Depends(get_user_repository),
):
    try:
        new_user = await users.create(u=user)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already registered with this email address"
        )
    return new_user


@router.patch("/",
              response_model=User,
              response_model_exclude={"hashed_password"},
              responses={
                  404: {
                      "description": "Not Found",
                  },
              },
              )
async def update_user(
        user_id: int,
        user: UserIn,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)
):
    try:
        old_user = await users.get_by_id(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User was not found")

    if old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    user = await users.update(user_id=user_id, u=user)
    return user
