from enum import Enum, auto, unique


@unique
class HeaderLabelType(Enum):
    RS = 'rs'
    METHOD = 'mt'
    STATUSCODE = 'sc'
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
    BAD = 'BAD_FORMAT'
    UNAUTHORIZED = 'UNAUTHORIZED'


@unique
class SCodeType(Enum):
    BADCONSTRUCTION = 10
    FunctionNotImplemented = 11
    UNAUTHORIZED = 12
