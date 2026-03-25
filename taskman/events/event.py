from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TaskEvent:
    kind: str  # 'created' | 'completed' | 'deleted'
    task_id: int
    title: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
