# Backward compatibility wrapper - imports moved to taskman.events module
from taskman.events.observers import LogObserver

__all__ = ['LogObserver']
