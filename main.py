import sys
from taskman.exceptions import TaskNotFoundError, StorageError, ValidationError, ConfigError, TaskManError
from rich.console import Console

from taskman.cli import main

from taskman.config import Config, handle_config_set, ConfigError
from taskman.themes import get_theme
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