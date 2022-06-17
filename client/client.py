from binascii import b2a_hqx
import json
import os
from socket import socket
from threading import Thread
from time import sleep
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

        self._username = None
        self._token = None

        self._chat_current = None
        self._chat_last_update = 0
        self._chat_messages = []

        self._menu_is_visible = False

        frame_info = self._get_server_info_crypt()

        # self._pub_k, self._pv_k = rsa.newkeys(
        #    frame_info.get_header().get_data()[HeaderLabelType.RSA.value])

        server_pub_k_str = str(frame_info.get_header().get_data()
                               [HeaderLabelType.PUBLICKEY.value]).split(' ')

        # self._server_pub_k = rsa.PublicKey(
        #    int(server_pub_k_str[0]), int(server_pub_k_str[1]))

        # print(self._pub_k, self._pv_k)
        # print(self._server_pub_k)

        print('----- Chat -----')
        self._init_username()
        print(f'Token: {self._token}', end='\n\n')

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

        thread = Thread(target=self._input_thread)
        thread.start()

        while True:

            if (not self._menu_is_visible
                and self._token is not None
                    and self._chat_current is not None):

                moment = self._chat_last_update

                header = FrameHeader({
                    HeaderLabelType.RS.value: 12,
                    HeaderLabelType.METHOD.value: 16,
                    HeaderLabelType.LASTUPDATE.value: moment,
                    HeaderLabelType.KEY.value: self._token,
                    HeaderLabelType.ROOMKEY.value: self._chat_current,
                })

                res = self._send_action(Frame(header, FrameBody()))

                if len(res.get_body().get_data()) > 0:
                    self._chat_messages.extend(res.get_body().get_data())
                    print(self._chat_messages)

                self._chat_last_update = res.get_header().get_data()[
                    HeaderLabelType.TIME.value]

                sleep(2)

    def _input_thread(self) -> None:

        chat_key = None

        while True:
            data = input()

            if data == '/menu':
                self._menu_is_visible = True

                self._print_menu()
                opt = int(input('Digite: '))

                if opt == 1:
                    self._menu_create_chat()
                elif opt == 2:
                    self._menu_list_chat()
                    input('Pressione enter para sair...')
                elif opt == 3:
                    chat_key = input('Chat key: ')
                    self._menu_join_chat(chat_key)
                elif opt == 4:
                    self._menu_info_chat()
                    input('Pressione enter para sair...')

                self._chat_last_update = 0
                self._menu_is_visible = False

                os.system('clear')

                print('----- Chat -----')
                print(f'Digite seu username: {self._username}')
                print(f'Token: {self._token}', end='\n\n')

                continue

            header = FrameHeader({
                HeaderLabelType.RS.value: 12,
                HeaderLabelType.METHOD.value: 12,
                HeaderLabelType.KEY.value: self._token,
                HeaderLabelType.ROOMKEY.value: self._chat_current,
            })

            self._send_action(Frame(header, FrameBody({'text': data})))

    def _init_username(self) -> None:

        self._username = input('Digite seu username: ')

        header = FrameHeader({
            HeaderLabelType.RS.value: 10,
            HeaderLabelType.METHOD.value: 11,
            HeaderLabelType.KEY.value: self._username,
        })

        frame_res = self._send_action(Frame(header, FrameBody()))
        self._token = frame_res.get_header().get_data()[
            HeaderLabelType.KEY.value]

    def _menu_create_chat(self) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 12,
            HeaderLabelType.KEY.value: self._token,
        })

        frame_res = self._send_action(Frame(header, FrameBody()))
        chat_key = frame_res.get_header().get_data()[
            HeaderLabelType.ROOMKEY.value]

        print(f'Chat Key: {chat_key}')

    def _menu_list_chat(self) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 16,
        })

        frame_res = self._send_action(Frame(header, FrameBody()))
        chats = frame_res.get_body().get_data()

        for i, c in enumerate(chats):
            print(f'{i}: {c}')

    def _menu_join_chat(self, chat_key: str) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 14,
            HeaderLabelType.KEY.value: self._token,
            HeaderLabelType.ROOMKEY.value: chat_key
        })

        frame_res = self._send_action(Frame(header, FrameBody()))
        self._chat_current = chat_key

    def _menu_info_chat(self) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 16,
            HeaderLabelType.KEY.value: self._token,
            HeaderLabelType.ROOMKEY.value: self._chat_current
        })

        frame_res = self._send_action(Frame(header, FrameBody()))

        for c in frame_res.get_body().get_data():
            uuid = c['uuid']
            owner = c['owner']
            print(f'- uuid: {uuid} | owner: {owner}')

            for u in c['users']:
                print(f'   - {u}')
            print()

    def _print_menu(self) -> None:
        print('[1] Criar Chat')
        print('[2] Listar Chat')
        print('[3] Entrar em um Chat')
        print('[4] Info. Chat')
