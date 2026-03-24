from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional
from .validators import validate_title, validate_due_date, validate_priority


class Task:
    count:int = 0
    def __init__(self, title:str, done:bool =False, id:int=-1):
        self.title = validate_title(title)
        self.done = done
        if (id == -1):
            self.id=Task.count
            Task.count+=1
        else:
            self.id=id

    def complete(self):
        self.done = True

    def __str__(self)-> str:
        mark = "[X]" if self.done else "[ ]"
        return f"{mark} {self.id}: {self.title}"

    def __repr__(self) -> str:
        return f"Task ( id = {self.id}, title= {self.title!r} )"



class DeadlineTask(Task):
    def __init__ (self,title:str, due_date:str, done:bool=False, id:int=-1):
        super().__init__(title, done, id)
        self.due_date = validate_due_date(due_date)

    def is_overdue(self) -> bool:
        return date.today() > datetime.strptime(self.due_date, "%Y-%m-%d").date()
    
    def __str__(self) -> str:
        overdue = " [OVERDUE]" if self.is_overdue() else ""
        return f"{super().__str__()} due: {self.due_date}{overdue}"


class PriorityTask(Task):
    def __init__( self, title:str, priority:int=1,
    done:bool=False, id:int=-1):
        super().__init__(title,done,id)
        self.priority = validate_priority(priority)

    def bump_priority(self) -> None:
        self.priority = validate_priority(min(self.priority + 1, 5))

    def __str__(self) -> str:
        stars = "*" * self.priority
        return f"{super().__str__()} priority: {stars}"