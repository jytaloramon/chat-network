import json
from typing import Dict, List

from protocol.protocoltypes import HeaderLabelType


class FrameHeader:

    def __init__(self, data_mapper: Dict) -> None:

        self._data: Dict[str, any] = {k.value: None for k in HeaderLabelType}

        self._mapper(data_mapper)

    def get_data(self) -> Dict[str, any]:

        return {
            k: i
            for k, i in self._data.items()
            if i is not None
        }

    def _mapper(self, data: Dict):

        for h in self._data.keys():
            item = data.get(h)
            if item is not None:
                self._data[h] = item


class FrameBody:

    def __init__(self, data: Dict[str, any] | List[Dict[str, any]] = None) -> None:

        self._data = data

    def get_data(self) -> any:

        return self._data


class Frame:

    def __init__(self, header: FrameHeader, body:  FrameBody) -> None:

        self._data: dict[str, FrameHeader | FrameBody] = {
            'header': header, 'body': body}

    def get_data(self) -> dict[str, FrameHeader | FrameBody]:

        return self._data

    def get_header(self) -> FrameHeader:

        return self._data.get('header')

    def get_body(self) -> FrameBody:

        return self._data.get('body')

    def __str__(self) -> str:
        header = self.get_header().get_data()
        body = self.get_body().get_data() if self.get_body().get_data() is not None else None

        return json.dumps({
            'header': header,
            'body':  body
        })
