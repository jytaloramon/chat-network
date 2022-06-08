import json
from socket import socket
from typing import Dict, Tuple
from framework.error import BadConstructionError, FunctionNotImplementedError
from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, SCodeType
from framework.router import RouterManager
from framework.serverthreadpool import ServerThreadPool
from time import time_ns


class ChatFramework:

    def __init__(self, host: str, port: int, router_manager: RouterManager) -> None:

        self._len_buffer = 2048
        self._backlog = 50
        self._router_manager = router_manager

        self._server_connection: socket = socket()
        self._server_connection.bind((host, port))
        self._server_connection.listen(self._backlog)

        print(f'Server UP [{host}:{port}]')

        self._thread_pool = ServerThreadPool(self._client_connection)

        self._run_connection_accept()

    def _run_connection_accept(self):

        while True:
            client_s, _ = self._server_connection.accept()
            self._thread_pool.add(client_s, self._len_buffer)

    def _client_connection(self, client_s: socket, len_buffer: int):

        data = client_s.recv(len_buffer)
        header, body = self._data_to_frame(data)
        req_frame = Frame(header, body)

        res_fram: Frame = None

        try:
            res_fram: Frame = self._router_manager.solver(req_frame)
        except BadConstructionError as bc:
            header_f = FrameHeader({
                HeaderLabelType.TIME.value: time_ns(),
                HeaderLabelType.STATUSCODE.value: SCodeType.BADCONSTRUCTION.value,
            })

            res_fram = Frame(header_f, FrameBody())
        except FunctionNotImplementedError as fni:
            header_f = FrameHeader({
                HeaderLabelType.TIME.value: time_ns(),
                HeaderLabelType.STATUSCODE.value: SCodeType.FunctionNotImplemented.value,
            })

            res_fram = Frame(header_f, FrameBody())

        client_s.send(bytes(res_fram.__str__(), 'UTF-8'))
        client_s.close()

    def _data_to_frame(self, data: bytes) -> Tuple[Dict, Dict]:

        frame = json.loads(data)

        return frame['header'], frame['body']
