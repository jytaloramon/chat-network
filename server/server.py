from framework.chatframework import ChatFramework
from server.routes import router_manager


class Server:

    def __init__(self, host: str, port: int) -> None:

        self._chat_framework = ChatFramework(host, port, router_manager)
