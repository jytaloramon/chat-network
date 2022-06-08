from typing import Callable, Dict, List, List
from framework.error import BadConstructionError, FunctionNotImplementedError

from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import HeaderLabelType, MethodType


class Router:

    def __init__(self, id: int, label: str) -> None:

        self._id = id
        self._label = label
        self._methods = {}

    def get_id(self) -> int:
        return self._id

    def get_label(self) -> str:
        return self._label

    def get_routine(self, mt_id: int):

        return self._methods.get(mt_id)

    def auth(self, func: Callable[[any, any], Frame]):
        self._methods[MethodType.AUTH.value] = func


class RouterManager:

    def __init__(self) -> None:

        self._routes: Dict[int, Router] = {}

    def get_routes(self) -> Dict[int, Router]:

        return self._routes

    def solver(self, frame: Frame) -> Frame:

        hearder = frame.get_header()

        rs = hearder.get(HeaderLabelType.RS.value)

        if rs is None:
            raise BadConstructionError('Recurso não informado')

        if rs == 1:
            return Frame(FrameHeader({'tt': 'kp'}), FrameBody(self._get_rss()))

        mt = hearder.get(HeaderLabelType.METHOD.value)

        if mt is None:
            raise BadConstructionError('Método não informado')

        router = self._routes[rs]

        if router is None or MethodType(mt) is None:
            raise BadConstructionError('Recurso não encontrado')

        routine = router.get_routine(mt)

        if routine is None:
            raise FunctionNotImplementedError(
                'Recurso não localizado/implementado')

        return routine(frame)

    def _get_rss(self) -> List[Dict[str, any]]:

        return [{'id': id, 'label': self._routes[id].get_label()}
                for id in self._routes.keys()]

    def add_router(self, router: Router):

        if router is None:
            raise Exception('Controler não pode ser nulo')

        if router.get_id() == 1:
            raise Exception('ID reservado para controle')

        if not(self._routes.get(router.get_id()) is None):
            raise Exception('Recurso com esse id já existe')

        self._routes[router.get_id()] = router
