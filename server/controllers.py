import math
from random import random
from time import time_ns
from tokenize import Token
from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, SCodeType
from server.entities import UserEntity
from server.repositories import UserAuthRepository, masterRepo
from uuid import uuid4


def user_auth(frame: Frame) -> Frame:

    body = frame.get_body()
    user = UserEntity(body['username'])

    repo: UserAuthRepository = masterRepo['userauthrepo']
    token = uuid4().__str__()

    repo.add(token, user)

    return Frame(
        FrameHeader({
            HeaderLabelType.STATUSCODE.value: SCodeType.SUCCESS.value,
            HeaderLabelType.TIME.value: time_ns(),
            HeaderLabelType.TOKEN.value: token 
        }), FrameBody())
