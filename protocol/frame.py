import json


class Frame:

    def __init__(self, header: dict[str, any], body:  dict[str, any]) -> None:

        self._data: dict[str, dict[str, any]] = {
            'header': header, 'body': body}

    def get_data(self) -> dict[str, dict[str, any]]:

        return self._data

    def get_header(self):

        return self._data.get('header')

    def get_body(self):

        return self._data.get('body')

    def __str__(self) -> str:

        return json.dumps(self._data)


class FrameHeader:

    def __init__(self) -> None:
        pass


class FrameBody:

    def __init__(self) -> None:
        pass
