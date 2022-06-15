from enum import Enum, unique


@unique
class HeaderLabelType(Enum):
    RS = 'rs'           # int
    METHOD = 'mt'       # int
    STATUSCODE = 'sc'   # int
    TIME = 'tm'         # str
    KEY = 'key'         # str
    ROOMKEY = 'rmk'     # str
    PUBLICKEY = 'apk'   # str
    RSA = 'rsa'         # int
    LASTUPDATE = 'ltu'  # str


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
    BADCONSTRUCTION = 'FRAME_BAD_CONSTRUCTION'
    FUNCNOTIMPLEMENTED = 'FUNC_NOT_IMPLEMENTED'
    SUCCESS = 'SUCESS'
    FAILURE = 'FAILURE'
    UNAUTHORIZED = 'UNAUTHORIZED'


@unique
class SCodeType(Enum):
    BADCONSTRUCTION = 10
    FUNCNOTIMPLEMENTED = 11
    SUCCESS = 20
    FAILURE = 30
    UNAUTHORIZED = 31
