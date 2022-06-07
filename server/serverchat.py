import json
from socket import socket
from typing import Dict
from protocol.frame import Frame
from server.router import RouterManager
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
        req_frame = self._data_to_frame(data)

        res_fram: Frame = self._router_manager.solver(req_frame)
        client_s.send(bytes(res_fram.__str__(), 'UTF-8'))
        client_s.close()

    def _data_to_frame(self, data: bytes) -> Dict:

        frame = json.loads(data)

        return frame
