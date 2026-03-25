from typing import Callable, List
from .event import TaskEvent

class EventBus:
    _listeners: List[Callable] = []

    @classmethod
    def subscribe(cls, fn: Callable) -> None:
        cls._listeners.append(fn)

    @classmethod
    def publish(cls, event: TaskEvent) -> None:
        for fn in cls._listeners:
            fn(event)
