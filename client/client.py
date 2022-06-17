from binascii import b2a_hqx
import json
from socket import socket
from threading import Thread
from typing import Dict, Tuple
from requests import head
import rsa
from protocol.frame import Frame, FrameHeader, FrameBody
from protocol.protocoltypes import HeaderLabelType


class ClientChat:

    def __init__(self, host: str, port: int, ) -> None:

        self._host = host
        self._port = port

        self._len_buffer = 4096
        self._token = None

        frame_info = self._get_server_info_crypt()

        # self._pub_k, self._pv_k = rsa.newkeys(
        #    frame_info.get_header().get_data()[HeaderLabelType.RSA.value])

        server_pub_k_str = str(frame_info.get_header().get_data()
                               [HeaderLabelType.PUBLICKEY.value]).split(' ')

        # self._server_pub_k = rsa.PublicKey(
        #    int(server_pub_k_str[0]), int(server_pub_k_str[1]))

        #print(self._pub_k, self._pv_k)
        # print(self._server_pub_k)

        self._init_username()
        print(f'Autenticado: {self._token}')

        self._chat()

    def _get_server_info_crypt(self) -> Frame:

        header = FrameHeader({
            HeaderLabelType.RS.value: 1,
            HeaderLabelType.METHOD.value: 11,
        })

        return self._send_action(Frame(header, FrameBody()))

    def _send_action(self, frame: Frame, is_encrypted: bool = False) -> Frame:

        connection = socket()
        connection.connect((self._host, self._port))

        msg = (rsa.encrypt(frame.__str__(), self._server_pub_k)
               if is_encrypted else frame.__str__())

        data_send = bytes(msg, 'utf-8')

        connection.send(data_send)
        resp = connection.recv(self._len_buffer)

        if is_encrypted:
            resp = self._decrypt_data(resp)

        resp_h, resp_b = self._data_to_frame(resp)

        connection.close()
        return Frame(FrameHeader(resp_h), FrameBody(resp_b))

    def _data_to_frame(self, data: bytes) -> Tuple[Dict, Dict]:

        frame = json.loads(data)

        return frame['header'], frame['body']

    def _decrypt_data(self, data: bytes) -> bytes:

        return rsa.decrypt(data, self._pv_k)

    def _chat(self) -> None:

        Thread()

        while True:
            pass

    def _input_thread(self) -> None:

        chat_key = None

        while True:
            data = input()
            if data == '/menu':
                pass

            header = FrameHeader({

            })

            self._send_action(Frame(header, FrameBody({'text': data})))

    def _init_username(self) -> None:

        username = input('Digite seu username: ')

        header = FrameHeader({
            HeaderLabelType.RS.value: 10,
            HeaderLabelType.METHOD.value: 11,
            HeaderLabelType.KEY.value: username,
        })

        frame_res = self._send_action(Frame(header, FrameBody()))
        self._token = frame_res.get_header().get_data()[
            HeaderLabelType.KEY.value]
