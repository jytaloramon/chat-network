from email import message
from typing import Dict, List
from uuid import uuid4

from server.errors import NotFoundError


class UserEntity:

    def __init__(self, name: str) -> None:

        self._name = name

    def get_name(self) -> str:

        return self._name


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


class RoomChatEntity:

    def __init__(self, id: str, name: str) -> None:

        self._id = id
        self._name = name
        self._users: List[UserEntity] = []
        self._messages: List[MessageEntity] = []

    def get_id(self) -> str:

        return self._id

    def get_name(self) -> str:

        return self._name

    def get_users(self) -> List[UserEntity]:

        return self._users

    def add_user(self, user: UserEntity) -> None:

        self._users.append(user)

    def get_messages(self, time_min=0) -> List[MessageEntity]:

        return list(filter(lambda x: x.get_moment() >= time_min, self._messages))

    def add_message(self, msg: MessageEntity) -> None:

        self._messages.append(msg)


class ChatEntity:

    def __init__(self) -> None:

        self._chat_rooms: Dict[str, RoomChatEntity] = {}
        self._users: Dict[str, UserEntity] = {}

    def get_chat_rooms(self) -> Dict[str, RoomChatEntity]:

        return self._chat_rooms

    def get_chat_room_by_id(self, id: str) -> RoomChatEntity:

        if self._chat_rooms.get(id) is None:
            return None

        return self._chat_rooms[id]

    def get_users(self) -> Dict[str, UserEntity]:

        return self._users

    def get_user_by_id(self,  id: str) -> Dict[str, UserEntity]:

        return self._users[id]

    def new_user(self, id: str, user: UserEntity) -> None:

        self._users[id] = user

    def new_room(self, room_chat: RoomChatEntity) -> None:

        self._chat_rooms[room_chat.get_id()] = room_chat

    def join_room(self, id_room: str, id_user: str):

        if self._chat_rooms.get(id_room) is None:
            raise NotFoundError('Sala não encontrada')

        if self._users.get(id_user) is None:
            raise NotFoundError('User não encontrada')

        room = self._chat_rooms[id_room]
        room.add_user(self._users[id_user])
