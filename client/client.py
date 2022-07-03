from binascii import b2a_hqx
import json
import os
from socket import socket
from threading import Thread
from time import sleep
from typing import Dict, Tuple
import rsa
from protocol.frame import Frame, FrameHeader, FrameBody, FrameWrapper
from protocol.protocoltypes import HeaderLabelType
from Crypto.Cipher import AES


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

        self._pub_k, self._pv_k = rsa.newkeys(2048)

        self._aes_cipher = None
        self._aes_decipher = None

        frame_info = self._get_session_server()
        key_session = str(
            frame_info.get_header().get_data()[HeaderLabelType.KEY.value]).split(' ')

        self._uuid_session = key_session[0]
        self._aes_key = bytes(key_session[1], 'UTF-8')
        iv = bytes(key_session[2], 'UTF-8')
        self._aes_cipher = AES.new(self._aes_key, AES.MODE_CFB, iv)
        self._aes_decipher = AES.new(
            self._aes_key, AES.MODE_CFB, iv)

        print('----- Chat -----')
        self._init_username()
        print(f'Session UUID: {self._uuid_session}')
        print(f'Token: {self._token}', end='\n\n')

        self._chat()

    def _get_session_server(self) -> Frame:

        header = FrameHeader({
            HeaderLabelType.RS.value: 1,
            HeaderLabelType.METHOD.value: 11,
            HeaderLabelType.PUBLICKEY.value: str(
                self._pub_k.n) + ' ' + str(self._pub_k.e)
        })

        return self._send_action(Frame(header, FrameBody()))

    def _send_action(self, frame: Frame, ids: str = '', enc: str = '') -> Frame:

        connection = socket()
        connection.connect((self._host, self._port))

        frame_wr = FrameWrapper({'ids': ids, 'enc': enc})

        data_send: bytes = None

        if frame_wr.get_data()['enc'] == '':
            data_send = bytes(frame_wr.__str__() + '\t\t' +
                              frame.__str__(), 'UTF-8')
        else:
            data_send = bytes(frame_wr.__str__(), 'UTF-8') + b'\t\t' + \
                self._encrypt_data(bytes(frame.__str__(), 'UTF-8'))

        connection.send(data_send)
        res_wr_data, resp_data = connection.recv(
            self._len_buffer).split(b'\t\t')

        connection.close()

        frame_wr_res = self._data_to_frame_wr(res_wr_data)
        frame_res: Frame = None

        if frame_wr_res.get_data()['enc'] == '':
            frame_res = self._data_to_frame(resp_data)
        elif frame_wr_res.get_data()['enc'] == 'rsa':
            frame_res = self._data_to_frame(
                self._decrypt_rsa_data(resp_data))
        else:
            frame_res = self._data_to_frame(self._decrypt_data(resp_data))

        status = frame_res.get_header().get_data()[
            HeaderLabelType.STATUSCODE.value]

        if status in (20, 21, 25, 26, 27):
            err = frame_res.get_header().get_data()[
                HeaderLabelType.ERROR.value]
            print(f'ERROR: {err}')

            input('Pressione enter para sair...')

            return None

        return frame_res

    def _data_to_frame_wr(self, data: bytes) -> FrameWrapper:

        frame = json.loads(data)

        return FrameWrapper(frame)

    def _data_to_frame(self, data: bytes) -> Frame:

        frame = json.loads(data)

        return Frame(FrameHeader(frame['header']), FrameBody(frame['body']))

    def _encrypt_data(self, data: bytes) -> bytes:

        return self._aes_cipher.encrypt(data)

    def _decrypt_rsa_data(self, data: bytes) -> bytes:

        return rsa.decrypt(data, self._pv_k)

    def _decrypt_data(self, data: bytes) -> bytes:

        return self._aes_decipher.decrypt(data)

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

                res = self._send_action(Frame(header, FrameBody()), self._uuid_session, 'aes')

                if len(res.get_body().get_data()) > 0:
                    if self._chat_last_update == 0:
                        for i in res.get_body().get_data():
                            username = i['username']
                            text = i['text']
                            moment_msg = i['moment']

                            if username != self._username:
                                print(f'> {username} - {text} [{moment_msg}]')
                            else:
                                print(f'> my - {text} [{moment_msg}]')
                        self._chat_messages = res.get_body().get_data()
                    else:
                        for i in res.get_body().get_data():
                            for i in res.get_body().get_data():
                                username = i['username']
                                text = i['text']
                                moment_msg = i['moment']

                                if username != self._username:
                                    print(
                                        f'> {username} - {text} [{moment_msg}]')

                        self._chat_messages.extend(res.get_body().get_data())

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

                os.system('clear')

                self._chat_last_update = 0
                self._menu_is_visible = False

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

            self._send_action(Frame(header, FrameBody({'text': data})), self._uuid_session, 'aes')

    def _init_username(self) -> None:

        while True:
            self._username = input('Digite seu username: ')

            header = FrameHeader({
                HeaderLabelType.RS.value: 10,
                HeaderLabelType.METHOD.value: 11,
                HeaderLabelType.KEY.value: self._username,
            })

            frame_res = self._send_action(
                Frame(header, FrameBody()), self._uuid_session, 'aes')

            if frame_res is not None:
                self._token = frame_res.get_header().get_data()[
                    HeaderLabelType.KEY.value]
                break

    def _menu_create_chat(self) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 12,
            HeaderLabelType.KEY.value: self._token,
        })

        frame_res = self._send_action(
            Frame(header, FrameBody()), self._uuid_session, 'aes')

        if frame_res is None:
            return

        chat_key = frame_res.get_header().get_data()[
            HeaderLabelType.ROOMKEY.value]

        print(f'Chat Key: {chat_key}')

    def _menu_list_chat(self) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 16,
        })

        frame_res = self._send_action(
            Frame(header, FrameBody()), self._uuid_session, 'aes')

        if frame_res is None:
            return

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

        frame_res = self._send_action(
            Frame(header, FrameBody()), self._uuid_session, 'aes')

        if frame_res is None:
            return

        self._chat_current = chat_key

    def _menu_info_chat(self) -> None:

        header = FrameHeader({
            HeaderLabelType.RS.value: 11,
            HeaderLabelType.METHOD.value: 16,
            HeaderLabelType.KEY.value: self._token,
            HeaderLabelType.ROOMKEY.value: self._chat_current
        })

        frame_res = self._send_action(
            Frame(header, FrameBody()), self._uuid_session, 'aes')

        if frame_res is None:
            return

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
