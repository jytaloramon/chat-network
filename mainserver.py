from protocol.frame import Frame
from framework.router import RouterManager, Router
from framework.chatframework import ChatFramework


def func_t(header, body) -> Frame:
    print(header, body)
    return Frame({},{})


def main():

    HOST = 'localhost'
    PORT = 7533

    router = Router(10, 'user')
    router.auth(func_t)

    router_manager = RouterManager()
    router_manager.add_router(router)

    server = ChatFramework(HOST, PORT, router_manager)


def func(header, body):
    pass


main()
