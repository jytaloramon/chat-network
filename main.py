from socket import socket

from protocol.frame import Frame
from protocol.protocoltypes import MethodType

t = socket()

t.connect(('localhost', 7533))

frame = Frame({'resourse': '/aut', 'method': MethodType.AUTH.value}, {})

print(frame.__str__())

t.send(bytes(frame.__str__(), 'UTF-8'))
d = t.recv(2048)
print(d)