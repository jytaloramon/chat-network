from server.routes import Routes
from server.serverchat import ServerChat


def main():

    HOST = 'localhost'
    PORT = 7533

    server = ServerChat(HOST, PORT, Routes('/'))


main()
