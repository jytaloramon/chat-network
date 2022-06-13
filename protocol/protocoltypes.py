from enum import Enum, auto, unique


@unique
class HeaderLabelType(Enum):
    RS = 'rs'
    METHOD = 'mt'
    STATUSCODE = 'sc'
    TIME = 'tm'
    KEY = 'ky'
    LASTUPDATE = 'lu'


@unique
class MethodLabelType(Enum):
    AUTH = 'auth'
    PUSH = 'push'
    PULL = 'pull'
    JOIN = 'join'


@unique
class MethodType(Enum):
    AUTH = 11
    PUSH = 12
    PULL = 16
    JOIN = 14


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
