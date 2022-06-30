from typing import Callable, Dict, List, List, Tuple
from framework.error import BadConstructionError, FunctionNotImplementedError

from protocol.frame import Frame, FrameBody, FrameHeader, FrameWrapper
from protocol.protocoltypes import HeaderLabelType, MethodType, SCodeType


class Router:

    def __init__(self, label: str, id: int = 1) -> None:

        self._id: int = id
        self._label: str = label
        self._methods: Dict[int, Callable] = {}

    def get_id(self) -> int:
        return self._id

    def get_label(self) -> str:
        return self._label

    def get_methods(self) -> Dict[int, Callable]:
        return self._methods

    def get_routine(self, mt_id: int):
        return self._methods.get(mt_id)

    def auth(self, func: Callable[[Frame], Tuple[FrameWrapper, bytes]]):
        self._methods[MethodType.AUTH.value] = func

    def push(self, func: Callable[[Frame], Tuple[FrameWrapper, bytes]]):
        self._methods[MethodType.PUSH.value] = func

    def pull(self, func: Callable[[Frame], Tuple[FrameWrapper, bytes]]):
        self._methods[MethodType.PULL.value] = func

    def join(self, func: Callable[[Frame], Tuple[FrameWrapper, bytes]]):
        self._methods[MethodType.JOIN.value] = func


class RouterManager:

    def __init__(self, router_controller: Router = None) -> None:

        self._routes: Dict[int, Router] = {}

        if router_controller is not None:
            self._routes[1] = router_controller

    def get_routes(self) -> Dict[int, Router]:

        return self._routes

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

    def solver(self, frame: Frame) -> Tuple[FrameWrapper, bytes]:

        hearder = frame.get_header()
        rs = hearder.get_data()[HeaderLabelType.RS.value]

        if rs is None:
            raise BadConstructionError('Recurso não informado')

        if rs == 1 and self._routes.get(1) is None:
            return Frame(
                FrameHeader({'sc': SCodeType.SUCCESS.value}),
                FrameBody(self._get_rss())
            )

        mt = hearder.get_data()[HeaderLabelType.METHOD.value]

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
