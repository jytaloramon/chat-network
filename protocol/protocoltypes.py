from enum import Enum, auto, unique


@unique
class HeaderLabelType(Enum):
    RS = 'rs'
    METHOD = 'mt'
    STATUSCODE = 'sc'
    TIME = 'tm'
    TOKEN = 'tk'
    LASTUPDATE = 'lu'


@unique
class MethodLabelType(Enum):
    AUTH = 'auth'


@unique
class MethodType(Enum):
    AUTH = 11


@unique
class SCodeLabelType(Enum):
    BADCONSTRUCTION = 'BAD_FORMAT'
    FunctionNotImplemented = ''
    UNAUTHORIZED = 'UNAUTHORIZED'


@unique
class SCodeType(Enum):
    BADCONSTRUCTION = 10
    FUNCNOTIMPLEMENTED = 11
    SUCCESS=20
    UNAUTHORIZED = 12
