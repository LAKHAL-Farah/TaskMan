from .models import Task, DeadlineTask, PriorityTask

class TaskDisplayDecorator:
    """Wraps a Task and adds display behaviour."""
    def __init__(self, task: Task):
        self._task = task

    def __getattr__(self, name):
        # delegate all attribute access to the wrapped task
        return getattr(self._task, name)

    def __str__(self) -> str:
        return str(self._task)


class OverdueDecorator(TaskDisplayDecorator):
    def __str__(self) -> str:
        base = super().__str__()
        return f'{base} [bold red]OVERDUE[/]'


class UrgentDecorator(TaskDisplayDecorator):
    def __str__(self) -> str:
        base = super().__str__()
        return f'[blink]{base}[/]'