from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query

from core.exceptions import UserNotFoundException, UserAlreadyExistsException
from models.user import User, UserIn
from repositories.users import UserRepository
from .depends import get_user_repository, get_current_user


router = APIRouter()


@router.get("/", response_model=List[User], response_model_exclude={"hashed_password"})
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = Query(
            default=100,
            title="Limit",
            description="Max size of returning list",
            ge=0,
            le=1000
        ),
        offset: int = Query(
            default=0,
            title="Offset",
            description="Amount  to skip",
            ge=0
        ),
):
    user_list = await users.get_all(limit=limit, offset=offset)
    return user_list


@router.post("/",
             response_model=User,
             response_model_exclude={"hashed_password"},
             responses={
                 409: {"description": "Account already exists"},
             },
             )
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
                  404: {"description": "User not Found"},
                  403: {"description": "Permission denied"},
              },
              )
async def update_user(
        user: UserIn,
        user_id: int = Query(
            default=0,
            title="User ID",
            description="""ID of 'User' to update\n
            0: - self, authenticated 'User'\n>
            1...: - ID of 'User'. Requires permission""",
            ge=0,
        ),
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)
):
    if not user_id:
        user_id = current_user.id

    try:
        old_user = await users.get_by_id(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User was not found")

    if old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    user = await users.update(user_id=user_id, u=user)
    return user
