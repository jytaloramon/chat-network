from time import time_ns
from typing import List, Tuple
from uuid import uuid4

import rsa

from server.entities import AppEntity, ChatEntity, MessageEntity, UseRegEntity, UserEntity
from server.errors import DuplicateError, NotFoundError
from rsa import PublicKey
from Crypto.Cipher import AES


class AppUseCases:

    app = AppEntity()

    def __init__(self) -> None:
        self.app = AppUseCases.app

    def new_session(self) -> Tuple[str, str]:

        session_id = uuid4().__str__()

        aes_key = uuid4().__str__()[:32]
        cipher = AES.new(bytes(aes_key, 'UTF-8'), AES.MODE_CFB)
        decipher = AES.new(bytes(aes_key, 'UTF-8'), AES.MODE_CFB, cipher.iv)

        self.app.add_aes_key(session_id, cipher, decipher)

        return (session_id, aes_key)

    def rsa_encrypt(self, n: int, e: int, data: str) -> bytes:

        pub_k = PublicKey(n, e)

        return rsa.encrypt(bytes(data, 'UTF-8'), pub_k)

    def aes_encrypt(self, uuid: str, data: str) -> bytes:

        aes = self.app.get_aes_key(uuid)

        if aes is None:
            raise NotFoundError('Sessão não existe')

        cipher = aes[0]

        return cipher.encrypt(bytes(data, 'UTF-8'))

    def aes_decrypt(self, uuid: str, data: bytes) -> bytes:

        aes = self.app.get_aes_key(uuid)

        if aes is None:
            raise NotFoundError('Sessão não existe')

        decipher = aes[1]

        return decipher.decrypt(data)

    def new_user(self, name: str) -> str:

        user = self.app.get_user_by_name(name)

        if user is not None:
            raise DuplicateError('Usuário já existe')

        user = UserEntity(name)
        uuid = uuid4().__str__()
        user_reg = UseRegEntity(uuid, user)

        self.app.add_user(user)
        self.app.add_users_reg(uuid, user_reg)

        return uuid

    def new_chat(self, uuid_user: str) -> str:

        user_reg = self.app.get_users_reg_by_uuid(uuid_user)

        if user_reg is None:
            raise NotFoundError('Usuário não existe')

        uuid = uuid4().__str__()
        chat = ChatEntity(uuid, user_reg.get_user())
        self.app.add_chat(uuid, chat)

        return uuid

    def join_user_chat(self, uuid_user: str, uuid_chat: str) -> None:

        user_reg = self.app.get_users_reg_by_uuid(uuid_user)

        if user_reg is None:
            raise NotFoundError('Usuário não existe')

        chat = self.app.get_chats_by_uuid(uuid_chat)

        if chat is None:
            raise NotFoundError('Chat não existe')

        chat.add_user(user_reg.get_uuid(), user_reg.get_user())

    def get_chats(self) -> List[ChatEntity]:

        return self.app.get_chats()

    def send_message_chat(self, uuid_user: str, uuid_chat: str, text: str) -> None:

        user_reg = self.app.get_users_reg_by_uuid(uuid_user)

        if user_reg is None:
            raise NotFoundError('Usuário não existe')

        chat = self.app.get_chats_by_uuid(uuid_chat)

        if chat is None:
            raise NotFoundError('Chat não existe')

        if chat.get_user_by_uuid(uuid_user) is None:
            raise Exception('Usuário não faz parte de chat')

        message = MessageEntity(text, user_reg.get_user(), time_ns())

        chat.add_message(message)

    def get_messages_chat(self, uuid_user: str, uuid_chat: str, from_moment: int = 0) -> List[MessageEntity]:

        user_reg = self.app.get_users_reg_by_uuid(uuid_user)

        if user_reg is None:
            raise NotFoundError('Usuário não existe')

        chat = self.app.get_chats_by_uuid(uuid_chat)

        if chat is None:
            raise NotFoundError('Chat não existe')

        if chat.get_user_by_uuid(uuid_user) is None:
            raise NotFoundError('Usuário não faz parte de chat')

        return chat.get_messages(from_moment)
