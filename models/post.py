import datetime
from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    id: Optional[str] = None
    user_id: Optional[int] = None
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PostIn(BaseModel):
    content: str
