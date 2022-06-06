import json
from pickle import FRAME
from socket import socket
from typing import Dict, List
from protocol.frame import Frame
from protocol.protocoltypes import CodeType, HeaderNameType, MethodNameType, MethodType
from server.routes import RouterManager, Routes
from server.serverthreadpool import ServerThreadPool


class ServerChat:

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
        frame = self._data_to_frame(data)

        rs = frame.get(HeaderNameType.RESOURCE.value)
        mt = frame.get(HeaderNameType.METHOD.value)

        res: Frame = None

        if rs is not None:
            if rs == MethodType.RSS:
                res = Frame({},{'data':})
        else:
            frame_res = Frame(
                {f'{HeaderNameType.STATUSCODE.value}': CodeType.BAD.value},
                {'info': f'Falta:{HeaderNameType.PATH.value}, {HeaderNameType.METHOD.value}'}
            )

        client_s.send(bytes(res.__str__(), 'UTF-8'))
        client_s.close()

    def _data_to_frame(self, data: bytes) -> Dict:
        frame = json.loads(data)

        return frame
