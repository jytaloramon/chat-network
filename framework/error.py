class BadConstructionError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class FunctionNotImplementedError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
