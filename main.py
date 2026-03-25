import sys
from taskman.exceptions import TaskNotFoundError, StorageError, ValidationError, ConfigError, TaskManError
from rich.console import Console

from taskman.cli import main

from taskman.config import Config, ConfigError
from taskman.config import get_theme

from taskman.events import EventBus
from taskman.events import LogObserver

LOG_PATH = 'history.log'
EventBus.subscribe(LogObserver(LOG_PATH))
cfg = Config.load()
theme = get_theme(cfg)
console = Console()

if __name__ == "__main__":
    try:
        main()
    except TaskNotFoundError as e:
        console.print(f"[red]Error:[/] {e}")
    except StorageError as e:
        console.print(f"[red]Storage error:[/] {e}")
        sys.exit(1)
    except ValidationError as e:
        console.print(f"[yellow]Invalid input:[/] {e}")
    except ConfigError as e:
        console.print(f"[red]Configuration error:[/] {e}")
        sys.exit(1)
    except TaskManError as e:
        # fallback for any other TaskMan errors
        console.print(f"[red]TaskMan error:[/] {e}")