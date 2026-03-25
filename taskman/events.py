from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, List

@dataclass
class TaskEvent:
    kind: str  # 'created' | 'completed' | 'deleted'
    task_id: int
    title: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class EventBus:
    _listeners: List[Callable] = []

    @classmethod
    def subscribe(cls, fn: Callable) -> None:
        cls._listeners.append(fn)

    @classmethod
    def publish(cls, event: TaskEvent) -> None:
        for fn in cls._listeners:
            fn(event)