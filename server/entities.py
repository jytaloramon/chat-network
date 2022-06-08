from typing import List


class UserEntity:

    def __init__(self, name: str) -> None:

        self._name = name

    def get_name(self) -> str:

        return self._name


class Message:

    def __init__(self, content: str, user: UserEntity, moment: int) -> None:

        self._content = content
        self._user = user
        self._moment = moment


class Chat:

    def __init__(self, id: int, name: str, moment: int) -> None:

        self._id = id
        self._name = name
        self._moment = moment
        self.messages: List[Message] = []
