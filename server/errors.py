class NotFoundError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class DuplicateError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)