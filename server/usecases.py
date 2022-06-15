from typing import List, Tuple
from uuid import uuid4
from server.entities import AppEntity, ChatEntity, UseRegEntity, UserEntity
from server.errors import NotFoundError
from rsa import PublicKey, PrivateKey

app = AppEntity()


class AppUseCases:

    def __init__(self) -> None:
        pass

    def get_rsa(self) -> Tuple[PublicKey, PrivateKey]:

        return (app.get_pub_key(), app.get_pv_key())

    def new_user(self, name: str) -> str:

        user = app.get_user_by_name(name)

        if user is not None:
            raise Exception('Usuário já existe')

        user = UserEntity(name)
        uuid = uuid4().__str__()
        user_reg = UseRegEntity(uuid, user)

        app.add_user(user)
        app.add_users_reg(user_reg)

        return uuid

    def new_chat(self, uuid_user: str, name_char: str) -> str:

        user_reg = app.get_users_reg_by_uuid(uuid_user)

        if user_reg is None:
            raise Exception('Usuário não existe')

        uuid = uuid4().__str__()
        chat = ChatEntity(uuid, user_reg.get_user())
        app.add_chat(uuid, chat)

        return uuid

    def join_user_chat(self, uuid_user: str, uuid_chat: str) -> None:

        user_reg = app.get_users_reg_by_uuid(uuid_user)

        if user_reg is None:
            raise Exception('Usuário não existe')

        chat = app.get_chats_by_uuid(uuid_chat)

        if chat is None:
            raise Exception('Chat não existe')

        chat.add_user(user_reg.get_uuid(), user_reg.get_user())

    def get_chats(self) -> List[ChatEntity]:

        return app.get_chats()
