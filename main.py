import json
from operator import le
from socket import socket

import rsa

from protocol.frame import Frame, FrameBody, FrameHeader, WrapperFrame
from protocol.protocoltypes import MethodType


t = socket()

t.connect(('localhost', 7533))

pub_k, pv_k = rsa.newkeys(2048)

frame = Frame(FrameHeader(
    {
        'rs': 1,
        'act': 16,
        'ltu': 1655408232734985444,
        'apk': ' '.join([str(pub_k.n), str(pub_k.e)])
    }),
    FrameBody()
)

wra = WrapperFrame(frame, {'enc': '', 'ids': '8b501a70-8147-4a84-90d3-a4cdac769a65'})

print(wra.__str__())

t.send(bytes(wra.__str__(), 'utf-8'))
d = t.recv(4096)
t.close()

data_j = json.loads(d)

print(data_j)

# Tested
# - controller = auth, pull
# - user = auth
#   - ed2bdd45-c134-4990-8a91-1f3e3f86f0f0
# - chat = push
#   - b0f0b874-7ed1-4f83-b21a-fbd7a739cc05
#   - 7dc4f54f-b62a-4a92-b192-f2436925819a
