import json
from socket import socket
from typing import Dict, Tuple

import rsa
from framework.error import BadConstructionError, FunctionNotImplementedError
from protocol.frame import Frame, FrameBody, FrameHeader, WrapperFrame
from protocol.protocoltypes import HeaderLabelType, PreHeaderLabelType, SCodeType
from framework.router import RouterManager
from framework.serverthreadpool import ServerThreadPool
from time import time_ns

from server.routes import use_case


class ChatFramework:

    def __init__(self, host: str, port: int, router_manager: RouterManager) -> None:

        self._len_buffer = 4096
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
        wrap_f = self._data_to_frame(data)

        frame_req = wrap_f.get_frame()

        wframe_res = self._router_manager.solver(frame_req)

        frame_encrypt = wframe_res.get_frame()

        # if wframe_res.get_data()['enc'] == 'rsa':
        #    keys_p = str(frame_req.get_header().get_data()['apk']).split(' ')

        #    frame_encrypt = self._encrypt_frame_rsa(
        #        int(keys_p[0]), int(keys_p[1]), wframe_res.get_frame().__str__())

        if wframe_res.get_data()['enc'] == 'aes':
            ids = wrap_f.get_data()['ids']

            frame_encrypt = str(self._encrypt_frame_aes(
                ids, bytes(wframe_res.get_frame().__str__(), 'utf-8')))

        wframe_res._data['frame'] = frame_encrypt

        client_s.send(bytes(wframe_res.__str__(), 'UTF-8'))
        client_s.close()

        self._log(data_inp, frame_req, wframe_res)
        self._req_id += 1

    def _data_to_frame(self, data: bytes) -> WrapperFrame:

        data_f = json.loads(data)

        ids = data_f[PreHeaderLabelType.IDSESSION.value]
        enc = data_f[PreHeaderLabelType.ENCRYPT.value]

        if enc == 'aes':
            f_data = self._decrypt_data_aes(ids, data_f['frame'])
            data_f['frame'] = f_data

        return WrapperFrame(
            Frame(FrameHeader(data_f['frame']['header']),
                  FrameBody(data_f['frame']['body'])),
            {'enc': data_f['enc'], 'ids': data_f['ids']}
        )

    def _decrypt_data_aes(self, uuid: str, data: bytes) -> bytes:

        return use_case.aes_decrypt(uuid, data)

    def _encrypt_frame_aes(self, uuid: str, data: bytes) -> bytes:

        return use_case.aes_encrypt(uuid, data)

    def _encrypt_frame_rsa(self, rsa_n: int,  rsa_e: int, data: bytes) -> bytes:

        pub_k = rsa.PublicKey(rsa_n, rsa_e)

        return rsa.encrypt(data, pub_k)

    def _log(self, data_inp: bytes, frame_req: Frame, frame_res: Frame) -> None:

        print(f'Request: {self._req_id} []')
        print(f' - {data_inp}')
        print(f' - {frame_req.__str__()}')
        print(f' - {frame_res.__str__()}')
        print('\n\n')
