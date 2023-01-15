from functools import wraps
from types import FunctionType

from databases import Database

from core.exceptions import DatabaseConnectionFailException


def database_connection(method):
    @wraps(method)
    async def wrapped(*args, **kwargs):
        try:
            response = await method(*args, **kwargs)
            return response
        except Exception as ex:
            connection_fail_string = "[Errno 10061] Connect call failed"
            if connection_fail_string in str(ex):
                raise DatabaseConnectionFailException(connection_fail_string)
    return wrapped


class MetaClass(type):
    def __new__(mcs, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if isinstance(attribute, FunctionType):
                # excluding 'magic' methods from wrapping xD
                if attributeName.startswith('__') and attributeName.endswith('__'):
                    attribute = attribute
                else:
                    attribute = database_connection(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(mcs, classname, bases, newClassDict)


class BaseRepository(metaclass=MetaClass):
    def __init__(self, database: Database):
        self.database = database
