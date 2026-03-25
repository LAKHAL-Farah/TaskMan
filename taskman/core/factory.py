from typing import Optional
from .models import Task, DeadlineTask, PriorityTask
from taskman.validators import validate_title, validate_due_date, validate_priority
from taskman.exceptions import ValidationError

class TaskFactory:
    @classmethod
    def create(cls, title: str, due: Optional[str] = None, priority: Optional[int] = None) -> Task:
        title = validate_title(title)
        if due and priority:
            raise ValidationError("Cannot set both --due and --priority.")
        if due:
            return DeadlineTask(title, validate_due_date(due))
        if priority:
            return PriorityTask(title, validate_priority(priority))
        return Task(title)
