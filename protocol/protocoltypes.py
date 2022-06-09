from enum import Enum, auto, unique


@unique
class HeaderLabelType(Enum):
    RS = 'rs'
    METHOD = 'mt'
    STATUSCODE = 'sc'
    TIME = 'tm'
    TOKEN = 'tk'
    LASTUPDATE = 'lu'
    KEY = 'ky'
    UTIL = 'UT'


@unique
class MethodLabelType(Enum):
    AUTH = 'auth'


@unique
class MethodType(Enum):
    AUTH = 11
    CREATE = 12
    GET = 16
    LIST = 13
    JOIN = 14
    POST = 15


@unique
class SCodeLabelType(Enum):
    BADCONSTRUCTION = 'BAD_FORMAT'
    FunctionNotImplemented = ''
    UNAUTHORIZED = 'UNAUTHORIZED'


@unique
class SCodeType(Enum):
    BADCONSTRUCTION = 10
    FUNCNOTIMPLEMENTED = 11
    SUCCESS = 20
    UNAUTHORIZED = 12
