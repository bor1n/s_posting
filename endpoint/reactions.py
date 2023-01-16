from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.enums import ReactionType
from models.post import Post
from models.reaction import Reaction
from models.user import User
from repositories.posts import PostRepository
from repositories.reactions import ReactionRepository
from .depends import get_post_repository, get_current_user, get_reaction_repository

router = APIRouter()


@router.get("/", response_model=List[Post])  # todo: change response model
async def get(
        post_id: int = 0,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user),
        reactions: ReactionRepository = Depends(get_reaction_repository),
):
    post = await posts.get(post_id)
    post.has_view_permission(current_user_id=current_user.id)  # raises PermissionDeniedException
    counts = await reactions.get_count(post_id=post_id)
    return counts


@router.post("/", response_model=Reaction)
async def update_reaction(
        post_id: int,
        value: ReactionType,
        reactions: ReactionRepository = Depends(get_reaction_repository),
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)
):
    post = await posts.get(post_id)
    post.has_view_permission(current_user_id=current_user.id)  # raises PermissionDeniedException
    reaction = await reactions.get(current_user.id, post_id)
    if not reaction:
        reaction = await reactions.create(user_id=current_user.id, post_id=post_id, value=value)
    else:
        if reaction.value != value:
            reaction = await reactions.update(user_id=current_user.id, post_id=post_id, value=value)
        else:
            reaction.updated_at = await reactions.delete(user_id=current_user.id, post_id=post_id)
    return reaction


@router.patch("/",
              response_model=Reaction,
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
        reactions: ReactionRepository = Depends(get_reaction_repository),
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)
):
    post = await posts.get(post_id)
    post.has_view_permission(current_user_id=current_user.id)  # raises PermissionDeniedException
    reaction = await reactions.delete(user_id=current_user.id, post_id=post_id)
    return reaction
