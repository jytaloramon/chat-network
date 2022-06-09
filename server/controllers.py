import math
from random import random
from time import time_ns
from tokenize import Token

from requests import head
from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, SCodeType
from server.usecases import ChatUseCases, repo_use_cases


def user_auth(frame: Frame) -> Frame:

    body = frame.get_body()
    chat: ChatUseCases = repo_use_cases['chat']
    token = chat.auth_user(body['username'])

    return Frame(
        FrameHeader({
            HeaderLabelType.STATUSCODE.value: SCodeType.SUCCESS.value,
            HeaderLabelType.TIME.value: time_ns(),
            HeaderLabelType.TOKEN.value: token,
        }), FrameBody())


def chat_create(frame: Frame) -> Frame:

    header = frame.get_header()
    chat: ChatUseCases = repo_use_cases['chat']
    id = chat.create_room(header[HeaderLabelType.KEY.value])

    return Frame(
        FrameHeader({
            HeaderLabelType.STATUSCODE.value: SCodeType.SUCCESS.value,
            HeaderLabelType.TIME.value: time_ns(),
            HeaderLabelType.UTIL.value: id
        }), FrameBody())


def chat_list(frame: Frame) -> Frame:

    chat: ChatUseCases = repo_use_cases['chat']

    return Frame(
        FrameHeader({
            HeaderLabelType.STATUSCODE.value: SCodeType.SUCCESS.value,
            HeaderLabelType.TIME.value: time_ns(),
        }), FrameBody(chat.list_room()))


def chat_join(frame: Frame) -> Frame:

    header = frame.get_header()
    chat: ChatUseCases = repo_use_cases['chat']

    chat.join_user_room(header[HeaderLabelType.KEY.value],
                        header[HeaderLabelType.TOKEN.value])

    return Frame(
        FrameHeader({
            HeaderLabelType.STATUSCODE.value: SCodeType.SUCCESS.value,
            HeaderLabelType.TIME.value: time_ns(),
        }), FrameBody())


def chat_get_info_room(frame: Frame) -> Frame:

    header = frame.get_header()
    chat: ChatUseCases = repo_use_cases['chat']

    rooms = chat.get_info_room(header[HeaderLabelType.KEY.value])

    return Frame(
        FrameHeader({
            HeaderLabelType.STATUSCODE.value: SCodeType.SUCCESS.value,
            HeaderLabelType.TIME.value: time_ns(),
        }), FrameBody(rooms))
