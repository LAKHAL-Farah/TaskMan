from taskman.events import TaskEvent

class LogObserver:
    def __init__(self, log_path):
        self.path = log_path

    def __call__(self, event: TaskEvent) -> None:
        with open(self.path, 'a') as f:
            f.write(f'{event.timestamp} {event.kind}: {event.title}\n')