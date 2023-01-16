import datetime
from typing import Optional, Dict

from pydantic import BaseModel

from core.enums import Visibility, ReactionType
from core.exceptions import PermissionDeniedException


class BasePost(BaseModel):
    content: str
    visibility: Visibility

    class Config:
        use_enum_values = True


class Post(BasePost):
    id: Optional[str] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime.datetime]
    updated_at: datetime.datetime
    reactions: Optional[Dict[ReactionType, int]]  # = {reaction: 0 for reaction in ReactionType}  # todo: remove default value

    def has_view_permission(self, current_user_id: int):
        if self.visibility == Visibility.NOBODY:
            if current_user_id != self.user_id:
                raise PermissionDeniedException


class PostIn(BasePost):
    pass
