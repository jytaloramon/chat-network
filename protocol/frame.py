import json
from time import time_ns
from typing import Dict, List

from protocol.protocoltypes import HeaderLabelType, WrapperLabelType


class FrameHeader:

    def __init__(self, data_mapper: Dict = None) -> None:

        self._data: Dict[str, any] = {k.value: None for k in HeaderLabelType}

        if data_mapper is not None:
            self._mapper(data_mapper)

    def get_data(self) -> Dict[str, any]:

        if self._data.get(HeaderLabelType.TIME.value) is None:
            self._data[HeaderLabelType.TIME.value] = time_ns()

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

    def set_rs(self, rs: int):
        self._data[HeaderLabelType.RS.value] = rs

    def set_method(self, mt: int):
        self._data[HeaderLabelType.METHOD.value] = mt

    def set_status_code(self, sc: int):
        self._data[HeaderLabelType.STATUSCODE.value] = sc

    def set_time(self, tm: int):
        self._data[HeaderLabelType.TIME.value] = tm

    def set_key(self, key: str):
        self._data[HeaderLabelType.KEY.value] = key

    def set_room_key(self, rmk: str):
        self._data[HeaderLabelType.ROOMKEY.value] = rmk

    def set_apk(self, apk: str):
        self._data[HeaderLabelType.PUBLICKEY.value] = apk

    def set_rsa(self, rsa: int):
        self._data[HeaderLabelType.RSA.value] = rsa

    def set_last_update(self, lu: str):
        self._data[HeaderLabelType.LASTUPDATE.value] = lu

    def set_err(self, err: str):
        self._data[HeaderLabelType.ERROR.value] = err


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


class FrameWrapper:

    def __init__(self, data_mapper: Dict[str, any]) -> None:

        self._data: Dict[str, any] = {
            k.value: data_mapper[k.value] for k in WrapperLabelType}

    def get_data(self) -> Dict[str, any]:

        return self._data

    def set_ids(self, ids: str):
        self._data[WrapperLabelType.IDS.value] = ids

    def set_enc(self, enc: str):
        self._data[WrapperLabelType.ENC.value] = enc

    def __str__(self) -> str:

        return json.dumps(self.get_data())
