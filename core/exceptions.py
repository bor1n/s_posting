
class PermissionDeniedException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class PostNotFoundException(Exception):
    pass


class ReactionNotFoundException(Exception):
    pass


class DatabaseConnectionFailException(Exception):
    def __init__(self, msg):
        self.msg = msg
