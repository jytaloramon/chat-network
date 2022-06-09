import json
from time import time_ns
from protocol.protocoltypes import HeaderLabelType, MethodType, SCodeType
from protocol.frame import FrameHeader, Frame, FrameBody

#frame_h = FrameHeader({
#    HeaderLabelType.TIME.value: time_ns(),
#    HeaderLabelType.STATUSCODE.value: SCodeType.FunctionNotImplemented.value,
#})

#frame_b = FrameBody()

#frame = Frame(frame_h, frame_b)
print(HeaderLabelType)
for i in HeaderLabelType:
    print(i.value)