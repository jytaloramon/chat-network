from typing import List
from framework.router import Router, RouterManager
from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, SCodeType
from server.usecases import ChatUseCases, repo_use_cases


def router_controller(routes_all: List[Router]) -> Router:
    router = Router('controller')

    def auth(frame_req=Frame) -> Frame:

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_apk('public key')

        return Frame(header_res, FrameBody())

    def pull(frame_req=Frame) -> Frame:

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        return Frame(header_res, FrameBody([
            {'id': r.get_id(), 'label': r.get_label(),
             'methods': list(r.get_methods().keys())}
            for r in routes_all
        ]))

    router.auth(auth)
    router.pull(pull)

    return router


def router_user() -> Router:
    router = Router('user', 10)

    def auth(frame: Frame) -> Frame:

        chat: ChatUseCases = repo_use_cases['chat']
        username = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        token = chat.auth_user(username)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_key(token)

        return Frame(header_res, FrameBody())

    router.auth(auth)

    return router


def router_chat() -> Router:
    router = Router('chat', 11)

    def create(frame: Frame) -> Frame:

        name_room = frame.get_body().get_data()['room']
        chat: ChatUseCases = repo_use_cases['chat']
        id = chat.create_room(name_room)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_room_key(id)

        return Frame(header_res, FrameBody())

    def pull(frame: Frame) -> Frame:

        chat: ChatUseCases = repo_use_cases['chat']
        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        return Frame(header_res, FrameBody(chat.list_room()))

    router.push(create)
    router.pull(pull)

    return router


routes_all = [
    router_user(),
    router_chat(),
]

router_manager = RouterManager(router_controller(routes_all))
for i in routes_all:
    router_manager.add_router(i)
