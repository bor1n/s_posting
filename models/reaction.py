import datetime

from pydantic import BaseModel

from core.enums import ReactionType


class Reaction(BaseModel):
    user_id: int
    post_id: int
    value: ReactionType
    updated_at: datetime.datetime

    class Config:
        use_enum_values = True
