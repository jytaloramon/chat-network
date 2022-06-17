from typing import List
from framework.router import Router, RouterManager
from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, SCodeType
from server.usecases import AppUseCases

use_case = AppUseCases()


def router_controller(routes_all: List[Router]) -> Router:

    router = Router('controller')
    routes = [router] + routes_all

    def auth(frame_req=Frame) -> Frame:

        pub_key, _ = use_case.get_rsa()

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_apk(str(pub_key.n) + ' ' + str(pub_key.e))
        header_res.set_rsa(2048)

        return Frame(header_res, FrameBody())

    def pull(frame_req=Frame) -> Frame:

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        return Frame(header_res, FrameBody([
            {'id': r.get_id(), 'label': r.get_label(),
             'methods': list(r.get_methods().keys())}
            for r in routes
        ]))

    router.auth(auth)
    router.pull(pull)

    return router


def router_user() -> Router:
    router = Router('user', 10)

    def auth(frame: Frame) -> Frame:

        username = frame.get_header().get_data().get_data()[
            HeaderLabelType.KEY.value]
        token = use_case.new_user(username)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_key(token)

        return Frame(header_res, FrameBody())

    router.auth(auth)

    return router


def router_chat() -> Router:
    router = Router('chat', 11)

    def push(frame: Frame) -> Frame:

        uuid_user = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        uuid_chat = use_case.new_chat(uuid_user)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_room_key(uuid_chat)

        return Frame(header_res, FrameBody())

    def pull(frame: Frame) -> Frame:

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        chats = [
            {'uuid': i.get_uuid(), 'owner': i.get_owner().get_name(),
             'users': [{'username': u.get_name()}for u in i.get_users()]
             } for i in use_case.get_chats()
        ]

        return Frame(header_res, FrameBody(chats))

    def join(frame: Frame) -> Frame:

        uuid_user = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        uuid_chat = frame.get_header().get_data()[
            HeaderLabelType.ROOMKEY.value]
        use_case.join_user_chat(uuid_user, uuid_chat)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        return Frame(header_res, FrameBody())

    router.push(push)
    router.pull(pull)
    router.join(join)

    return router


def router_message() -> Router:
    router = Router('message', 12)

    def push(frame: Frame) -> Frame:

        uuid_user = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        uuid_chat = frame.get_header().get_data()[
            HeaderLabelType.ROOMKEY.value]
        text = frame.get_body()['text']

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        use_case.send_message_chat(uuid_user, uuid_chat, text)

        return Frame(header_res, FrameBody())

    def pull(frame: Frame) -> Frame:

        uuid_user = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        uuid_chat = frame.get_header().get_data()[
            HeaderLabelType.ROOMKEY.value]
        last_update = frame.get_header().get_data()[
            HeaderLabelType.LASTUPDATE.value]

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        messages = [
            {'text': m.get_content(), 'moment': m.get_moment(),
             'username': m.get_user().get_name()}
            for m in use_case.get_messages_chat(uuid_user, uuid_chat, last_update)
        ]

        return Frame(
            header_res,
            FrameBody(messages)
        )

    router.push(push)
    router.pull(pull)

    return router


routes_all = [
    router_user(),
    router_chat(),
    router_message(),
]

router_manager = RouterManager(router_controller(routes_all))
for i in routes_all:
    router_manager.add_router(i)
