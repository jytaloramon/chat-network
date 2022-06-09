from typing import Dict
from uuid import uuid4
from server.entities import ChatEntity, RoomChatEntity, UserEntity
from server.errors import NotFoundError


class ChatUseCases:

    def __init__(self) -> None:

        self._chat_entity = ChatEntity()

    def auth_user(self, name: str) -> str:

        user = UserEntity(name)
        token = uuid4().__str__()

        self._chat_entity.new_user(token, user)

        return token

    def create_room(self, name: str) -> str:

        token = uuid4().__str__()
        room_chat = RoomChatEntity(token, name)

        self._chat_entity.new_room(room_chat)

        return token

    def list_room(self) -> Dict[str, any]:

        arr = []
        for k, i in self._chat_entity.get_chat_rooms().items():
            arr.append({'id': i.get_id(), 'name': i.get_name()})

        return arr

    def join_user_room(self, id_room: str, id_user) -> None:

        self._chat_entity.join_room(id_room, id_user)

    def get_info_room(self, id_room: str) -> Dict[str, any]:

        room = self._chat_entity.get_chat_room_by_id(id_room)

        if room is None:
            raise NotFoundError('Sala não encontrada')

        return {
            'id': room.get_id(),
            'name': room.get_name(),
            'users': room.get_users()
        }


repo_use_cases: Dict[str, any] = {
    'chat': ChatUseCases()
}
