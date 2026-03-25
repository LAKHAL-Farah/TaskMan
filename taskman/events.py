# Backward compatibility wrapper - imports moved to taskman.events module
from taskman.events.event import TaskEvent
from taskman.events.bus import EventBus
from taskman.events.observers import LogObserver

__all__ = ['TaskEvent', 'EventBus', 'LogObserver']
