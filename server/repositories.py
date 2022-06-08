from typing import Dict
from uuid import UUID
from server.entities import UserEntity


class UserAuthRepository:

    def __init__(self) -> None:

        self._users: Dict[str, UserEntity] = {}

    def get_user(self, token: str):

        return self._users.get(token)

    def add(self, token: str, user: UserEntity):

        self._users[token] = user


masterRepo: Dict[str, any] = {
    'userauthrepo': UserAuthRepository()
}
