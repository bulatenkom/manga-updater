from collections import deque
from queue import Queue
from typing import Any, Type, get_origin

def enc_hook(obj: Any) -> Any:
    if isinstance(obj, deque):
        return list(obj)
    if isinstance(obj, Queue):
        return list(obj.queue)
    else:
        raise NotImplementedError(f"Objects of type {type(obj)} are not supported")


def dec_hook(type: Type, obj: Any) -> Any:
    if get_origin(type) is deque:
        return deque(obj)
    if get_origin(type) is Queue:
        queue = Queue()
        queue.queue = deque(obj)
        return queue
    else:
        raise NotImplementedError(f"Objects of type {type} are not supported")