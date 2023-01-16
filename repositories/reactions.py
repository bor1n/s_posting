import datetime

from typing import List, Union, Dict

from databases.backends.postgres import Record
from sqlalchemy import func, funcfilter
from sqlalchemy.orm import Query
from sqlalchemy.sql import label

from core.enums import ReactionType
from core.exceptions import ReactionNotFoundException
from models.post import Post, PostIn
from models.reaction import Reaction
from .base import BaseRepository
from db.reactions import reactions


class ReactionRepository(BaseRepository):
    async def get_count(
            self,
            post_id: int = 0
    ) -> Dict[ReactionType, int]:
        query = Query([
            *[label(
                reaction.value,
                funcfilter(func.count(reactions.c.value), reactions.c.value == reaction)
            ) for reaction in ReactionType],
        ]).group_by(reactions.c.post_id).where(reactions.c.post_id == post_id)

        data = await self.database.fetch_one(query=query.statement)
        return {element: data[element] for element in data}

    async def get(self, user_id: int, post_id: int) -> Union[Reaction, None]:
        query = reactions.select().where(
            reactions.c.user_id == user_id,
            reactions.c.post_id == post_id
        )
        reaction = await self.database.fetch_one(query=query)
        if not reaction:
            return None
        return Reaction.parse_obj(reaction)

    async def create(self, user_id: int, post_id: int, value: ReactionType) -> Reaction:
        new_reaction = Reaction(
            user_id=user_id,
            post_id=post_id,
            value=value,
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**new_reaction.dict(exclude_unset=True)}

        query = reactions.insert().values(**values)
        await self.database.execute(query)
        return new_reaction

    async def update(self, user_id: int, post_id: int, value: ReactionType) -> Reaction:
        new_reaction = Reaction(
            user_id=user_id,
            post_id=post_id,
            value=value,
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**new_reaction.dict(exclude_unset=True)}
        # something is not clear, looks like a hack
        # a better idea is to use raw connection to check updated count, but I don't wanna
        query = reactions.update().where(
            reactions.c.user_id == user_id,
            reactions.c.post_id == post_id
        ).values(**values).returning(reactions.c.updated_at)
        updated_at_response = await self.database.execute(query)
        if not updated_at_response:  # means if UPDATE returned nothing with RETURNING in statement
            raise ReactionNotFoundException

        new_reaction.updated_at = updated_at_response
        return new_reaction

    async def delete(self, user_id: int, post_id: int) -> datetime.datetime:
        query = reactions.delete().where(
            reactions.c.user_id == user_id,
            reactions.c.post_id == post_id
        ).returning(reactions.c.updated_at)
        updated_at_response = await self.database.execute(query)
        if not updated_at_response:
            raise ReactionNotFoundException
        return updated_at_response
