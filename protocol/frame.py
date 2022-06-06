import json


class Frame:

    def __init__(self, header: dict[str, any], body:  dict[str, any]) -> None:

        self._data: dict[str, dict[str, any]] = {
            'header': header, 'body': body}

    def get_data(self) -> dict[str, dict[str, any]]:
        return self._data

    def __str__(self) -> str:
        return json.dumps(self._data)
