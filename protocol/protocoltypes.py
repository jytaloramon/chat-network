from enum import Enum, auto, unique


@unique
class HeaderLabelType(Enum):
    RS = 'rs'
    METHOD = 'mt'
    STATUSCODE = 'cs'
    TOKEN = 'tk'
    LASTUPDATE = 'lu'


@unique
class MethodLabelType(Enum):
    AUTH = 'auth'
    FIND = 'find'
    GET = 'getmsg'
    CREATE = 'create'
    JOIN = 'join'


@unique
class MethodType(Enum):
    AUTH = 11
    FIND = 20
    GET = 21
    CREATE = 30
    JOIN = 40


@unique
class CodeLabelType(Enum):
    BAD = 'BAD_FORMAT'
    UNAUTHORIZED = 'UNAUTHORIZED'


@unique
class CodeType(Enum):
    BAD = 10
    UNAUTHORIZED = 11
