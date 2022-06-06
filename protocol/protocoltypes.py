from enum import Enum, auto, unique


@unique
class MethodType(Enum):
    RSS = 10
    AUTH = 11
    FIND = 20
    GET = 21
    CREATE = 30
    JOIN = 40


@unique
class MethodNameType(Enum):
    RSS = 'resources'
    AUTH = 'auth'
    FIND = 'find'
    GET = 'getmsg'
    CREATE = 'create'
    JOIN = 'join'


@unique
class HeaderType(Enum):
    RESOURCE = 10
    METHOD = 11
    CODESTATUS = 12
    TOKEN = 15
    LASTUPDATE = 16


@unique
class HeaderNameType(Enum):
    RESOURCE = 'rs'
    METHOD = 'mt'
    STATUSCODE = 'cs'
    TOKEN = 'tK'
    LASTUPDATE = 'LU'


@unique
class CodeNameType(Enum):
    BAD = 'BAD_FORMAT'
    UNAUTHORIZED = 'UNAUTHORIZED'


@unique
class CodeType(Enum):
    BAD = 10
    UNAUTHORIZED = 11
