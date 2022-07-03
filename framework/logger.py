from mimetypes import init
from typing import Dict, List, Tuple
from protocol.frame import Frame, FrameWrapper


class Logger:

    _data: Dict[int, List[Tuple[bytes, FrameWrapper, Frame]]] = {}

    def __init__(self) -> None:
        self.data = Logger._data

    def add_req(self, id: int, frame_req_b: bytes, wr_req: FrameWrapper, frame_req: Frame) -> None:
        data = (frame_req_b, wr_req, frame_req)
        self.data[id] = []
        self.data[id].append(data)

    def add_res(self, id: int, frame_res_b: bytes, wr_res: FrameWrapper, frame_res: Frame) -> None:
        data = (frame_res_b, wr_res, frame_res)
        self.data[id].append(data)

    def pop_data(self, id: int):
        req = self.data[id][0]
        res = self.data[id][1]

        print(f'Request: {id} []')
        print(f' - REQUET RAW (FRAME): {req[0]}', end='\n\n')
        print(f' - REQUET (WR): {req[1].get_data()}', end='\n\n')
        print(f' - REQUET (Frame): {req[2].__str__()}', end='\n\n')
        print(f' - RESPONSE (WR): {res[1].get_data()}', end='\n\n')
        print(f' - RESPONSE (Frame): {res[2].__str__()}', end='\n\n')
        print(f' - RESPONSE RAW (FRAME): {res[0]}', end='\n\n')
        print('--------------------\n\n')

        self.data.pop(id)
