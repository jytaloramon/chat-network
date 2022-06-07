from typing import Dict, List, List

from protocol.frame import Frame
from protocol.protocoltypes import HeaderLabelType, MethodType


class Router:

    def __init__(self, resource: int, label: str) -> None:

        self._resource = resource
        self._label = label

    def get_resource(self) -> int:
        return self._resource

    def get_label(self) -> str:
        return self._label

    def auth(self, func=None):
        self._methods[MethodType.AUTH.value] = func

    def find(self, func=None):
        self._methods[MethodType.FIND.value] = func


class RouterManager:

    def __init__(self) -> None:

        self._routes: Dict[int, Router] = {}

    def get_routes(self) -> Dict[int, Router]:

        return self._routes

    def solver(self, frame: Frame) -> Frame:

        hearder = frame.get('header')

        rs = hearder.get(HeaderLabelType.RS.value)

        if rs is None:
            raise Exception('Recurso não informado')

        if rs == 1:
            return Frame({}, {'data': self._get_rss()})

        mt = hearder.get(HeaderLabelType.METHOD.value)

        if mt is None:
            raise Exception('Método não informado')

    def _get_rss(self) -> List[Dict[str, any]]:

        return [{'id': id, 'label': self._routes[id].get_label()}
                for id in self._routes.keys()]

    def add_router(self, router: Router):

        if router is None:
            raise Exception('Controler não pode ser nulo')

        if router.get_resource() == 1:
            raise Exception('ID reservado para controle')

        if not(self._routes.get(router.get_resource()) is None):
            raise Exception('Recurso com esse id já existe')

        self._routes[router.get_resource()] = router
