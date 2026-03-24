# taskman/exceptions.py

class TaskManError(Exception):
    """Base — all TaskMan errors inherit from this."""


class TaskNotFoundError(TaskManError):
    def __init__(self, task_id: int):
        super().__init__(f'No task with id={task_id}')
        self.task_id = task_id


class StorageError(TaskManError):
    """Raised when JSON read/write fails."""


class ValidationError(TaskManError):
    """Raised when user input fails validation."""


class ConfigError(TaskManError):
    """Raised on bad config values."""