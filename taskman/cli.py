import argparse

from rich.console import Console
from rich.table import Table
from rich import box

from taskman.models import Task, DeadlineTask, PriorityTask
from taskman.storage import load_tasks, save_tasks


console = Console()
def handle_add(args,tasks):
    if args.due:
        task = DeadlineTask(args.title, args.due)
    elif args.priority:
        task = PriorityTask(args.title, args.priority)
    else:
        task = Task(args.title)
    tasks.append(task)
    save_tasks(tasks)

    console.print(f"[green]Added task:[/] {task}")


def handle_list(args, tasks):

    filtered = {
        'done': [t for t in tasks if t.done],
        'pending': [t for t in tasks if not t.done],
        'all': tasks
    }[args.filter]

    if not filtered:
        console.print("[yellow]No tasks to show[/]")
        return

    table = Table(
        box=box.ROUNDED,
        header_style="bold purple"
    )

    table.add_column("ID", width=4)
    table.add_column("Status", width=8)
    table.add_column("Title", min_width=22)
    table.add_column("Type", width=14)
    table.add_column("Extra", width=16)

    for task in filtered:

        done = "[green]done[/]" if task.done else "[dim]todo[/]"
        extra = ""

        if isinstance(task, DeadlineTask):
            col = "red" if task.is_overdue() else "yellow"
            extra = f"[{col}]{task.due_date}[/]"

        elif isinstance(task, PriorityTask):
            extra = "[magenta]" + "*" * task.priority + "[/]"

        table.add_row(
            str(task.id),
            done,
            task.title,
            type(task).__name__,
            extra
        )

    console.print(table)

    done_n = sum(1 for t in filtered if t.done)
    console.print(f"[dim]{done_n}/{len(filtered)} complete[/]")


def handle_done(args, tasks):
    task = next((t for t in tasks if t.id == args.id), None)
    if not  task:
        console.print(f"[red]Task with ID {args.id} not found[/]")
        return
    task.complete()
    save_tasks(tasks)
    console.print(f"[green]Task marked as done:[/] {task}")


def handle_delete(args, tasks):
    before = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == before:
        console.print(f"[red]Task with ID {args.id} not found[/]")
        return
    save_tasks(tasks)
    console.print(f"[green]Deleted task with ID {args.id}[/]")



def main():
    
    tasks = load_tasks()
    
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # add command
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("title")
    parser_add.add_argument("--due", help="Deadline YYYY-MM-DD")
    parser_add.add_argument("--priority", type=int, help="Priority level")
    
    # list command
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--filter", choices=["all","done","pending"], default="all")
    
    # done command
    parser_done = subparsers.add_parser("done")
    parser_done.add_argument("id", type=int)
    
    # delete command
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("id", type=int)
    
    args = parser.parse_args()
    
    if args.command == "add":
        handle_add(args, tasks)
    elif args.command == "list":
        handle_list(args, tasks)
    elif args.command == "done":
        handle_done(args, tasks)
    elif args.command == "delete":
        handle_delete(args, tasks)
    else:
        parser.print_help()