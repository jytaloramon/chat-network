from typing import List, Tuple

from requests import session
from framework.router import Router, RouterManager
from protocol.frame import Frame, FrameBody, FrameHeader, FrameWrapper
from protocol.protocoltypes import HeaderLabelType, SCodeType
from server.usecases import AppUseCases

use_case = AppUseCases()


def build_frame_res(ids: str, enc: str, frame: Frame, n: int = 0, e: int = 0) -> Tuple[FrameWrapper, bytes]:

    frame_wr = FrameWrapper({
        'ids': ids,
        'enc': enc,
    })

    if enc == '':
        return (frame_wr, bytes(frame.__str__(), 'UTF-8'))

    if enc == 'rsa':
        return (frame_wr, use_case.rsa_encrypt(n, e, frame.__str__()))

    return (frame_wr, use_case.aes_encrypt(ids, frame.__str__()))


def aes_decrypt(ids: str, data: bytes) -> bytes:

    return use_case.aes_decrypt(ids, data)


def router_controller(routes_all: List[Router]) -> Router:

    router = Router('controller')
    routes = [router] + routes_all

    def auth(frame_req: Frame) -> Tuple[FrameWrapper, bytes]:

        header = frame_req.get_header().get_data()
        n, e = list(
            map(int, str(header[HeaderLabelType.PUBLICKEY.value]).split(' ')))

        ss_uuid, aes, iv = use_case.new_session()

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_key(' '.join([ss_uuid, aes, iv]))
        frame_res = Frame(header_res, FrameBody())

        return build_frame_res('', 'rsa', frame_res, n, e)

    def pull(frame_req: Frame) -> Tuple[FrameWrapper, bytes]:

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        frame_res = Frame(header_res, FrameBody([
            {'id': r.get_id(), 'label': r.get_label(),
             'methods': list(r.get_methods().keys())}
            for r in routes
        ]))

        return build_frame_res('', '', frame_res)

    router.auth(auth)
    router.pull(pull)

    return router


def router_user() -> Router:
    router = Router('user', 10)

    def auth(frame: Frame) -> Tuple[FrameWrapper, bytes]:

        session_uuid = frame.get_header().get_data()['ids']
        username = frame.get_header().get_data()[
            HeaderLabelType.KEY.value]
        token = use_case.new_user(username)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_key(token)

        return build_frame_res(session_uuid, 'aes', Frame(header_res, FrameBody()))

    router.auth(auth)

    return router


def router_chat() -> Router:
    router = Router('chat', 11)

    def push(frame: Frame) -> Tuple[FrameWrapper, bytes]:

        session_uuid = frame.get_header().get_data()['ids']
        uuid_user = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        uuid_chat = use_case.new_chat(uuid_user)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)
        header_res.set_room_key(uuid_chat)

        return build_frame_res(session_uuid, 'aes', Frame(header_res, FrameBody()))

    def pull(frame: Frame) -> Tuple[FrameWrapper, bytes]:

        session_uuid = frame.get_header().get_data()['ids']
        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        chats = [
            {'uuid': i.get_uuid(), 'owner': i.get_owner().get_name(),
             'users': [{'username': u.get_name()}for u in i.get_users()]
             } for i in use_case.get_chats()
        ]

        return build_frame_res(session_uuid, 'aes', Frame(header_res, FrameBody(chats)))

    def join(frame: Frame) -> Tuple[FrameWrapper, bytes]:

        session_uuid = frame.get_header().get_data()['ids']
        uuid_user = frame.get_header().get_data()[HeaderLabelType.KEY.value]
        uuid_chat = frame.get_header().get_data()[
            HeaderLabelType.ROOMKEY.value]
        use_case.join_user_chat(uuid_user, uuid_chat)

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        return build_frame_res(session_uuid, 'aes', Frame(header_res, FrameBody()))

    router.push(push)
    router.pull(pull)
    router.join(join)

    return router


def router_message() -> Router:
    router = Router('message', 12)

    def push(frame: Frame) -> Tuple[FrameWrapper, bytes]:

        session_uuid = frame.get_header().get_data()['ids']
        uuid_user = frame.get_header().get_data().get(HeaderLabelType.KEY.value)
        uuid_chat = frame.get_header().get_data().get(HeaderLabelType.ROOMKEY.value)

        text = frame.get_body().get_data()['text']

        header_res = FrameHeader()
        header_res.set_status_code(SCodeType.SUCCESS.value)

        use_case.send_message_chat(uuid_user, uuid_chat, text)

        return build_frame_res(session_uuid, 'aes', Frame(header_res, FrameBody()))

    def pull(frame: Frame) -> Tuple[FrameWrapper, bytes]:

        session_uuid = frame.get_header().get_data()['ids']

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

        return build_frame_res(session_uuid, 'aes', Frame(
            header_res,
            FrameBody(messages)
        ))

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
