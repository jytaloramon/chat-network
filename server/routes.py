from pyclbr import Function
from typing import Dict, List, Optional

from protocol.protocoltypes import MethodType


class RoutesBase:

    def __init__(self, base_path: str, routes: List = []) -> None:

        if not(base_path[0] == '/'):
            raise Exception('path not init with "/"')

        self._base_path = base_path
        self._methods: Dict[int, Function] = {}

    def get_base_path(self) -> str:
        return self._base_path

    def auth(self, func: Function = None):
        pass

    def getmsg(self, func: Function = None):
        pass

    def sendmsg(self, func: Function = None):
        pass


class Routes(RoutesBase):

    def __init__(self, base_path: str, routes: List[RoutesBase] = []) -> None:

        if not(base_path[0] == '/'):
            raise Exception('path not init with "/"')

        super().__init__(base_path, routes)

        self._routes = Dict[str, routes] = dict(
            [(r.get_base_path(), r)for r in routes])

    def auth(self, func: Function = None):
        self._methods[MethodType.AUTH.value] = func

    def getmsg(self):
        pass

    def sendmsg(self):
        pass
