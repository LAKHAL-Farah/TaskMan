# taskman/sorters.py
from abc import ABC, abstractmethod
from typing import List
from taskman.models import Task

# --- Strategy Interface ---
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        ...

# --- Concrete Strategies ---
class ByPrioritySort(SortStrategy):
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: getattr(t, 'priority', 0), reverse=True)

class ByDueDateSort(SortStrategy):
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: getattr(t, 'due_date', '9999'))

class ByTitleSort(SortStrategy):
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.title.lower())

# --- Mapping for runtime selection ---
SORTERS = {
    'priority': ByPrioritySort(),
    'due': ByDueDateSort(),
    'title': ByTitleSort(),
}