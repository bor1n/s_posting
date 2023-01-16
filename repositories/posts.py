import datetime

from typing import List

from core.enums import ReactionType
from core.exceptions import PostNotFoundException
from models.post import Post, PostIn
from .base import BaseRepository
from db.posts import posts


class PostRepository(BaseRepository):
    async def list(self, user_id: int = 0, limit: int = 100, offset: int = 0) -> List[Post]:
        query = posts.select().limit(limit).offset(offset)
        if user_id:
            query.where(posts.c.user_id == user_id)
        return await self.database.fetch_all(query=query)

    async def get(self, post_id: int) -> Post:
        query = posts.select().where(posts.c.id == post_id)
        post = await self.database.fetch_one(query=query)
        if not post:
            raise PostNotFoundException
        return Post.parse_obj(post)

    async def create(self, user_id: int, post_in: PostIn) -> Post:
        new_post = Post(
            user_id=user_id,
            content=post_in.content,
            visibility=post_in.visibility,
            reactions={reaction: 0 for reaction in ReactionType},
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**new_post.dict(exclude_unset=True)}

        query = posts.insert().values(**values)
        new_post.id = await self.database.execute(query)
        return new_post

    async def update(self, post_id: int, post_in: PostIn) -> Post:
        post = Post(
            content=post_in.content,
            visibility=post_in.visibility,
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**post.dict(exclude_unset=True)}

        # something is not clear, looks like a hack
        # a better idea is to use raw connection to check updated count, but I don't wanna
        query = posts.update().where(posts.c.id == post_id).values(**values).returning(posts.c.updated_at)
        updated_at_response = await self.database.execute(query)
        if not updated_at_response:  # means if UPDATE returned nothing with RETURNING in statement
            raise PostNotFoundException

        post.updated_at = updated_at_response
        return post

    async def delete(self, post_id: int) -> int:
        query = posts.delete().where(posts.c.id == post_id).returning(posts.c.id)
        post_id = await self.database.execute(query)
        if not post_id:
            raise PostNotFoundException
        return post_id
