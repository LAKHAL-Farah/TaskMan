# Backward compatibility wrapper - imports moved to taskman.core
from taskman.core.repository import JsonTaskRepo, AbstractTaskRepository

__all__ = ['JsonTaskRepo', 'AbstractTaskRepository']
