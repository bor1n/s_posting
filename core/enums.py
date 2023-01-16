from pydantic.types import Enum


class Visibility(int, Enum):
    NOBODY = 0
    EVERYONE = 1


class ReactionType(str, Enum):
    DISLIKE = 'DISLIKE'
    LIKE = 'LIKE'
    JOPA = 'JOPA'
