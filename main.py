from socket import socket

from protocol.frame import Frame, FrameBody, FrameHeader, FrameWrapper
from protocol.protocoltypes import MethodType
import rsa

pub_k, pv_key = rsa.newkeys(2048)


t = socket()

t.connect(('localhost', 7533))

frame_wr = FrameWrapper({
    'ids': '',
    'enc': ''
})

frame = Frame(FrameHeader(
    {
        'rs': 1,
        'act': 16,
        'apk': str(pub_k.n) + ' ' + str(pub_k.e)
    }),
    FrameBody()
)

print(frame_wr.__str__())
print(frame.__str__())

t.send(bytes(frame_wr.__str__()+'\t\t'+frame.__str__(), 'UTF-8'))
d = t.recv(4096)
t.close()
print(d)

wr, f = d.split(b'\t\t')
f_res = rsa.decrypt(f, pv_key)

print('------')
print(wr)
print(f_res)



# Tested
# - controller = auth, pull
# - user = auth
#   - ed2bdd45-c134-4990-8a91-1f3e3f86f0f0
# - chat = push
#   - b0f0b874-7ed1-4f83-b21a-fbd7a739cc05
#   - 7dc4f54f-b62a-4a92-b192-f2436925819a
