from threading import Thread
from typing import List


class ServerThreadPool:

    def __init__(self, task) -> None:

        self._task = task
        self._threads: List[Thread] = []

    def add(self, data: any, len_buffer: int):

        thread_task = Thread(target=self._task, args=(data, len_buffer))
        thread_task.start()
        
        self._threads.append(thread_task)
