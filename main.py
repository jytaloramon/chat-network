from socket import socket

from protocol.frame import Frame, FrameBody, FrameHeader
from protocol.protocoltypes import MethodType

t = socket()

t.connect(('localhost', 7533))

frame = Frame(FrameHeader(
    {
        'rs': 12,
        'act': 16,
        'ltu': 1655408232734985444,
        'key': '18fcbe28-9f3e-4e85-b79d-f81233cfac2c',
        'chk': '1b2e8b0b-861e-4c46-9a48-03ade564e501'
    }),
    FrameBody({
        'text': 'ramon'
    })
)

print(frame.__str__())

t.send(bytes(frame.__str__(), 'UTF-8'))
d = t.recv(2048)
t.close()
print(d)

# Tested
# - controller = auth, pull
# - user = auth
#   - ed2bdd45-c134-4990-8a91-1f3e3f86f0f0
# - chat = push
#   - b0f0b874-7ed1-4f83-b21a-fbd7a739cc05
#   - 7dc4f54f-b62a-4a92-b192-f2436925819a
