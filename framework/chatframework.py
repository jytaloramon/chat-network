import json
from socket import socket
from typing import Dict, Tuple

import rsa
from framework.error import BadConstructionError, FunctionNotImplementedError
from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, SCodeType
from framework.router import RouterManager
from framework.serverthreadpool import ServerThreadPool
from time import time_ns
from server.errors import DuplicateError, NotFoundError

from server.routes import use_case


class ChatFramework:

    def __init__(self, host: str, port: int, router_manager: RouterManager) -> None:

        self._len_buffer = 2048
        self._backlog = 50
        self._router_manager = router_manager

        self._server_connection: socket = socket()
        self._server_connection.bind((host, port))
        self._server_connection.listen(self._backlog)

        self._req_id = 0

        print(f'Server UP [{host}:{port}]')

        self._thread_pool = ServerThreadPool(self._client_connection)

        self._run_connection_accept()

    def _run_connection_accept(self):

        while True:
            client_s, _ = self._server_connection.accept()
            self._thread_pool.add(client_s, self._len_buffer)

    def _client_connection(self, client_s: socket, len_buffer: int):

        data_inp = data = client_s.recv(len_buffer)

        if not(data[0] == ord('{') and data[-1] == ord('}')):
            data = self._decrypt_data(data)

        header, body = self._data_to_frame(data)
        frame_req = Frame(FrameHeader(header), FrameBody(body))

        frame_res: Frame = None

        try:
            frame_res: Frame = self._router_manager.solver(frame_req)
        except BadConstructionError as e:
            header_f = FrameHeader({
                HeaderLabelType.TIME.value: time_ns(),
                HeaderLabelType.STATUSCODE.value: SCodeType.BADCONSTRUCTION.value,
                HeaderLabelType.ERROR.value: e.args[0]
            })

            frame_res = Frame(header_f, FrameBody())
        except FunctionNotImplementedError as e:
            header_f = FrameHeader({
                HeaderLabelType.TIME.value: time_ns(),
                HeaderLabelType.STATUSCODE.value: SCodeType.FUNCNOTIMPLEMENTED.value,
                HeaderLabelType.ERROR.value: e.args[0]
            })

            frame_res = Frame(header_f, FrameBody())
        except NotFoundError as e:
            header_f = FrameHeader({
                HeaderLabelType.TIME.value: time_ns(),
                HeaderLabelType.STATUSCODE.value: SCodeType.FAILURE.value,
                HeaderLabelType.ERROR.value: e.args[0]
            })

            frame_res = Frame(header_f, FrameBody())

        except DuplicateError as e:
            header_f = FrameHeader({
                HeaderLabelType.TIME.value: time_ns(),
                HeaderLabelType.STATUSCODE.value: SCodeType.CONFLICT.value,
                HeaderLabelType.ERROR.value: e.args[0]
            })

            frame_res = Frame(header_f, FrameBody())

        client_s.send(bytes(frame_res.__str__(), 'UTF-8'))
        client_s.close()

        self._log(data_inp, frame_req, frame_res)
        self._req_id += 1

    def _data_to_frame(self, data: bytes) -> Tuple[Dict, Dict]:

        frame = json.loads(data)

        return frame['header'], frame['body']

    def _decrypt_data(self, data: bytes) -> bytes:

        _, pv_k = use_case.get_rsa()

        return rsa.decrypt(data, pv_k)

    def _log(self, data_inp: bytes, frame_req: Frame, frame_res: Frame) -> None:

        print(f'Request: {self._req_id} []')
        print(f' - {data_inp}')
        print(f' - {frame_req.__str__()}')
        print(f' - {frame_res.__str__()}')
        print('\n\n')
