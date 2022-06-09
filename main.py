from socket import socket

from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import MethodType

t = socket()

t.connect(('localhost', 7533))

frame = Frame(FrameHeader({'rs': 11, 'mt': 13, 'ky': 'Sala 1'}), FrameBody())

print(frame.__str__())

t.send(bytes(frame.__str__(), 'UTF-8'))
d = t.recv(2048)
t.close()
print(d)
