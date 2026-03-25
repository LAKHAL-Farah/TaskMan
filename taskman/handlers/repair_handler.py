from pathlib import Path
import shutil
from rich.console import Console
from taskman.core import DATA_FILE

console = Console()

def handle_repair(args, repo=None):
    """Restore the latest backup of tasks.json"""
    backups = sorted(DATA_FILE.parent.glob("*.bak"))

    if not backups:
        console.print("[yellow]No backups found.[/]")
        return

    latest = backups[-1]

    try:
        shutil.copy(latest, DATA_FILE)
        console.print(f"[green]Restored from {latest.name}[/]")
    except Exception as e:
        console.print(f"[red]Failed to restore backup: {e}[/]")

    if repo:
        repo.get_all()
