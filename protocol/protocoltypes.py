from enum import Enum, unique
from http.client import CONFLICT


@unique
class HeaderLabelType(Enum):
    RS = 'rs'           # int
    METHOD = 'act'      # int
    STATUSCODE = 'sc'   # int
    TIME = 'tm'         # str
    KEY = 'key'         # str
    ROOMKEY = 'chk'     # str
    PUBLICKEY = 'apk'   # str
    RSA = 'rsa'         # int
    LASTUPDATE = 'ltu'  # str
    ERROR = 'err'       # str


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
    FUNCNOTIMPLEMENTED = 'ACTION_NOT_IMPLEMENTED'
    FAILURE = 'FAILURE'
    CONFLICT = 'CONFLIT'
    UNAUTHORIZED = 'UNAUTHORIZED'
    SUCCESS = 'SUCESS'


@unique
class SCodeType(Enum):
    SUCCESS = 10
    BADCONSTRUCTION = 20
    FUNCNOTIMPLEMENTED = 21
    FAILURE = 25
    CONFLICT = 26
    UNAUTHORIZED = 27
