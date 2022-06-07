from server.router import RouterManager, Router
from server.serverchat import ServerChat


def main():

    HOST = 'localhost'
    PORT = 7533
    
    router_manager = RouterManager()
    router_manager.add_router(Router(10, 'ok'))

    server = ServerChat(HOST, PORT,router_manager)


main()
