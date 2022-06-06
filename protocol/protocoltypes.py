from enum import Enum, auto, unique


@unique
class MethodNameType(Enum):
    AUTH = 'auth'
    BAD_FORMAT = 'bad_format'
    GETMSG = 'getmsg'
    SENDMSG = 'sendmsg'


@unique
class MethodType(Enum):
    AUTH = 10
    BAD_FORMAT = 11
    GETMSG = 20
    SENDMSG = 30


@unique
class HeaderNameType(Enum):
    PATH = 'path'
    METHOD = 'method'
    CODE = 'code'
    TOKEN = '1'
    LASTUPDATE = '2'
    SENDMSG = '3'


@unique
class HeaderType(Enum):
    TOKEN = auto()
    LASTUPDATE = auto()
    SENDMSG = auto()


@unique
class CodeType(Enum):
    LOGIN = auto()
    GETMSG = auto()
    SENDMSG = auto()
