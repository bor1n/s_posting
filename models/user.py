import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, constr


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class User(BaseUser):
    id: Optional[int] = None
    hashed_password: str
    created_at: Optional[datetime.datetime]
    updated_at: datetime.datetime


class UserIn(BaseUser):
    password: constr(min_length=8)
    password2: constr(min_length=8)

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError("passwords don't match")
        return v
