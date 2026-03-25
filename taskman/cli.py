import argparse
from rich.console import Console
from taskman.core import Task, JsonTaskRepo, DATA_FILE
from taskman.commands import Command
from taskman.config import Config, get_theme, ConfigError
from taskman.events import EventBus, LogObserver
from taskman.handlers import (
    handle_add, handle_list, handle_done, handle_delete,
    handle_interactive, handle_stats, handle_repair, handle_config_set
)


# Initialize globals
cfg = Config.load()
theme = get_theme(cfg)
console = Console()
LOG_PATH = "history.log"
EventBus.subscribe(LogObserver(LOG_PATH))

history: list[Command] = []

def run(cmd: Command):
    """Execute a command and add to history for undo."""
    cmd.execute()
    history.append(cmd)

def undo_last():
    """Undo the last command executed."""
    if history:
        history.pop().undo()
        console.print("[green]Last action undone[/]")
    else:
        console.print("[yellow]Nothing to undo[/]")


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    parser.add_argument("--verbose", action="store_true", help="Show animated progress when loading tasks")

    subparsers = parser.add_subparsers(dest="command")

    # add command
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("title")
    parser_add.add_argument("--due", help="Deadline YYYY-MM-DD")
    parser_add.add_argument("--priority", type=int, help="Priority level")

    # list command
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--filter", choices=["all", "done", "pending"], default="all")
    parser_list.add_argument("--sort", choices=["priority", "due", "title"], help="Sort tasks by specified criteria")
    
    # done command
    parser_done = subparsers.add_parser("done")
    parser_done.add_argument("id", type=int)

    # delete command
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("id", type=int)

    # interactive command
    parser_interactive = subparsers.add_parser("interactive")

    # stats command
    parser_stats = subparsers.add_parser("stats")

    # repair command
    repair_parser = subparsers.add_parser("repair", help="Restore latest backup")

    # undo command
    parser_undo = subparsers.add_parser("undo", help="Undo last action")

    # config command
    parser_config = subparsers.add_parser("config", help="Manage config settings")
    parser_config.add_argument("--set", help="Set a config key=value")

    args = parser.parse_args()
    repo = JsonTaskRepo(DATA_FILE)  
    
    # Initialize Task.count from existing tasks
    existing_tasks = repo.get_all()
    if existing_tasks:
        Task.count = max(t.id for t in existing_tasks) + 1
    else:
        Task.count = 0

    # Route commands
    if args.command == "repair":
        handle_repair(args, repo)
    elif args.command == "config" and args.set:
        handle_config_set(args, None)
    elif args.command == "undo":
        undo_last()
    elif args.command == "add":
        handle_add(args, repo, theme, run)
    elif args.command == "list":
        handle_list(args, repo, theme)
    elif args.command == "done":
        handle_done(args, repo, theme, run)
    elif args.command == "delete":
        handle_delete(args, repo, theme, run)
    elif args.command == "stats":
        handle_stats(args, repo, theme)
    elif args.command == "interactive":
        handle_interactive(args, repo, theme, run, undo_last)
    else:
        parser.print_help()


