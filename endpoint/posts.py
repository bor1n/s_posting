from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.exceptions import UserNotFoundException
from models.post import Post, PostIn
from models.user import User
from repositories.posts import PostRepository
from .depends import get_post_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[Post])
async def list(
        posts: PostRepository = Depends(get_post_repository),
        user_id: int = 0,
        limit: int = 100,
        offset: int = 0,
):
    users = await posts.list(user_id=user_id, limit=limit, offset=offset)
    return users


@router.post("/", response_model=Post)
async def create(
        post: PostIn,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)
):
    new_post = await posts.create(user_id=current_user.id, post_in=post)
    return new_post


@router.patch("/",
              response_model=Post,
              responses={
                  404: {
                      "description": "Not Found",
                  },
                  403: {
                      "description": "Permission denied",
                  },
              },
              )
async def update(
        post_id: int,
        post: PostIn,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)
):
    try:
        old_post = await posts.get(post_id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post was not found")

    if current_user.id != old_post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    user = await posts.update(post_id=post_id, post_in=post)
    return user
