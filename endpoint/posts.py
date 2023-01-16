from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.enums import Visibility
from core.exceptions import UserNotFoundException
from models.post import Post, PostIn
from models.user import User
from repositories.posts import PostRepository
from repositories.reactions import ReactionRepository
from .depends import get_post_repository, get_current_user, get_reaction_repository

router = APIRouter()


@router.get("/list", response_model=List[Post])
async def list(
        posts: PostRepository = Depends(get_post_repository),
        user_id: int = 0,
        limit: int = 100,
        offset: int = 0,
):
    posts = await posts.list(user_id=user_id, limit=limit, offset=offset)
    return posts


@router.get("/", response_model=Post)
async def get(
        post_id: int,
        posts: PostRepository = Depends(get_post_repository),
        reactions: ReactionRepository = Depends(get_reaction_repository),
):
    post = await posts.get(post_id=post_id)
    if post.visibility != Visibility.EVERYONE:
        current_user = Depends(get_current_user)
        post.has_view_permission(current_user_id=current_user.id)
    post.reactions = await reactions.get_count(post_id=post_id)
    return post


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

    post = await posts.update(post_id=post_id, post_in=post)
    post.id = old_post.id
    post.reactions = old_post.reactions
    return post


@router.delete("/",
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
async def delete(
        post_id: int,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)
):
    try:
        old_post = await posts.get(post_id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post was not found")

    if current_user.id != old_post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    post = await posts.delete(post_id=post_id)
    return post
