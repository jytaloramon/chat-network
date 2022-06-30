from typing import Dict, List, Tuple
import rsa


class UserEntity:

    def __init__(self, name: str) -> None:

        self._name = name

    def get_name(self) -> str:

        return self._name


class UseRegEntity:

    def __init__(self, uuid: str, user: UserEntity) -> None:

        self._uuid = uuid
        self._user = user

    def get_uuid(self) -> str:

        return self._uuid

    def get_user(self) -> UserEntity:

        return self._user


class MessageEntity:

    def __init__(self, content: str, user: UserEntity, moment: int) -> None:

        self._content = content
        self._user = user
        self._moment = moment

    def get_content(self) -> str:

        return self._content

    def get_user(self) -> UserEntity:

        return self._user

    def get_moment(self) -> int:

        return self._moment


class ChatEntity:

    def __init__(self, uuid: str, owner: UserEntity) -> None:

        self._uuid = uuid
        self._owner: UserEntity = owner
        self._users: Dict[str, UserEntity] = {}
        self._messages: List[MessageEntity] = []

    def get_uuid(self) -> str:

        return self._uuid

    def get_owner(self) -> UserEntity:

        return self._owner

    def get_users(self) -> List[UserEntity]:

        return list(self._users.values())

    def get_user_by_uuid(self, uuid: str) -> UserEntity:

        if self._users.get(uuid) is None:
            return None

        return self._users[uuid]

    def add_user(self, uuid: str, user: UserEntity) -> None:

        self._users[uuid] = user

    def get_messages(self, from_moment: int = 0) -> List[MessageEntity]:

        return list(filter(lambda x: x.get_moment() >= from_moment, self._messages))

    def add_message(self, message: MessageEntity) -> None:

        self._messages.append(message)


class AppEntity:

    def __init__(self) -> None:

        self._chats: Dict[str, ChatEntity] = {}
        self._users: Dict[str, UserEntity] = {}
        self._users_reg: Dict[str, UseRegEntity] = {}
        self._aes_keys: Dict[str, Tuple[any, any, any]] = {}

    def add_aes_key(self, uuid: str, cipher: any, decipher: any, iv: any) -> None:

        self._aes_keys[uuid] = (cipher, decipher, iv)

    def get_aes_key(self, uuid: str) -> Tuple[any, any]:

        return self._aes_keys.get(uuid)

    def get_chats(self) -> List[ChatEntity]:

        return list(self._chats.values())

    def get_chats_by_uuid(self, uuid: str) -> ChatEntity:

        return self._chats.get(uuid)

    def add_chat(self, uuid: str, chat: ChatEntity) -> None:

        self._chats[uuid] = chat

    def get_users(self) -> List[UserEntity]:

        return list(self._users.values())

    def get_user_by_name(self, name: str) -> UserEntity:

        return self._users.get(name)

    def add_user(self, user: UserEntity) -> None:

        self._users[user.get_name()] = user

    def get_users_reg(self) -> List[UseRegEntity]:

        return list(self._users_reg.values())

    def get_users_reg_by_uuid(self, uuid: str) -> UseRegEntity:

        return self._users_reg.get(uuid)

    def add_users_reg(self, uuid: str, user: UseRegEntity) -> None:

        self._users_reg[uuid] = user
