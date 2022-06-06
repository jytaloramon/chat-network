from pyclbr import Function
from typing import Dict, List, Optional

from protocol.protocoltypes import MethodType


class Routes:

    def __init__(self, resource: int, label: str) -> None:

        self._resource = resource
        self._label = label

    def get_resource(self) -> int:
        return self._resource()

    def get_label(self) -> str:
        return self._label

    def auth(self, func: Function = None):
        self._methods[MethodType.AUTH.value] = func

    def find(self, func: Function = None):
        self._methods[MethodType.FIND.value] = func


class RouterManager:

    def __init__(self) -> None:

        self._routes: Dict[int, Routes] = {}

    def get_routes(self) -> Dict[int, Routes]:
        return self._routes

    def get_rss(self) -> Dict[int, Routes]->Dict[]:
        return [f'{id} - {r.get_label()}'for id, r in self._routes]


    def add_router(self, router: Routes):
        if not(self._routes.get(router.get_resource()) is None):
            raise Exception('Recurso com esse id já existe')

        self._routes[router.get_resource()] = router

    def get_routes_by_resource(self, id: int) -> Routes:
        return self._routes[id]

