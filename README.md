# TaskMan CLI
> A command-line task manager built with Python OOP, argparse, and JSON persistence.
## Features
- Add plain tasks, tasks with deadlines, or priority tasks
- List tasks with filters: all / done / pending
- Mark tasks complete, delete tasks
- Interactive mode with arrow-key navigation and actions
- Stats view showing totals, done, overdue, and by task type
- Colour-coded terminal output using **Rich** 
- Customizable themes: `default`, `minimal`, `dracula`
- Animated progress bars when loading tasks (`--verbose`)
- Tasks persist between sessions (JSON file in `~/.taskman/tasks.json`)
- **Custom exception hierarchy** (`TaskManError` base, `TaskNotFoundError`, `StorageError`, `ValidationError`, `ConfigError`)
- **Data validation**: titles, due dates, and priority fields are validated
- **Automatic recovery** from corrupted task files: backups created, valid tasks restored
- **Idempotent operations**: marking done twice or deleting non-existent tasks is safe
- **Robust error handling**: all storage and validation errors caught and reported gracefully
- **Event-driven logging**: Observer pattern with `EventBus` fires `TaskEvent` on task creation, completion, and deletion.
- **Persistent activity log**: All task events written to `~/.taskman/history.log` via `LogObserver`.
- Loose coupling for future extensions (e.g., adding email notifications or other observers without changing core logic)
- **Config management**: Modify CLI behavior via `python main.py config --set key=value` (e.g., change theme, default filter, date format)


## Usage
```bash
# Add tasks
python main.py add 'Buy milk'
python main.py add 'Submit report' --due 2026-04-01
python main.py add 'Fix bug' --priority 5

# List tasks
python main.py list
python main.py list --filter pending

# Mark done or delete
python main.py done 0
python main.py delete 1

# Interactive mode
python main.py interactive

# Show stats
python main.py stats

# Verbose mode with animated progress
python main.py list --verbose

# Repair corrupted tasks file
python main.py repair


# Config management
python main.py config --set theme=dracula
python main.py config --set default_filter=pending


# Event log
# Every task action fires an event and is logged automatically:
# Location of log file:
~/.taskman/history.log

# Example:
python main.py add "Buy milk"

```
## Architecture

The project is organized into focused, single-responsibility modules for clarity and maintainability.

### Directory Structure

```
taskman/
│
├── cli.py                # Entry point: argparse routing only (clean & minimal)
│
├── core/                 # Business logic & data layer
│   ├── __init__.py
│   ├── models.py         # Task, DeadlineTask, PriorityTask
│   ├── factory.py        # TaskFactory for task creation
│   ├── repository.py     # JsonTaskRepo, AbstractTaskRepository
│   ├── storage.py        # JSON persistence, error recovery
│   └── sorters.py        # Sort strategies
│
├── commands/             # Command pattern with undo
│   ├── __init__.py
│   ├── base.py          # Command ABC
│   ├── add.py           # AddTaskCommand
│   ├── complete.py      # CompleteTaskCommand
│   └── delete.py        # DeleteTaskCommand  
│
├── decorators/           # Display decorators
│   ├── __init__.py
│   └── display.py       # TaskDisplayDecorator, OverdueDecorator, UrgentDecorator
│
├── events/               # Event-driven logging
│   ├── __init__.py
│   ├── event.py         # TaskEvent dataclass
│   ├── bus.py           # EventBus publisher
│   └── observers.py     # LogObserver
│
├── config/               # Configuration & themes
│   ├── __init__.py
│   ├── config.py        # Config management
│   └── themes.py        # Theme definitions
│
└── handlers/             # CLI command handlers
    ├── __init__.py
    ├── add_handler.py           # handle_add()
    ├── list_handler.py          # handle_list()
    ├── done_handler.py          # handle_done()
    ├── delete_handler.py        # handle_delete()
    ├── interactive_handler.py   # handle_interactive()
    ├── stats_handler.py         # handle_stats()
    ├── repair_handler.py        # handle_repair()
    └── config_handler.py        # handle_config_set()
```

### Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| **core** | Business logic: task models, data access, sorting, factory pattern |
| **commands** | Reversible operations with undo support |
| **decorators** | Display enhancements (overdue flags, blinking urgent tasks) |
| **events** | Task event publishing and observer-based logging |
| **config** | Runtime settings, theme management, configuration persistence |
| **handlers** | CLI command implementations, Rich UI formatting, user interactions |
| **cli.py** | Argument parsing router that dispatches to handlers |

### Design Patterns Used

- **Factory**: `TaskFactory` creates appropriate task types
- **Strategy**: `SortStrategy` enables flexible task sorting
- **Command**: Command pattern with undo/redo history
- **Decorator**: Wraps tasks to enhance display (Overdue, Urgent)
- **Observer**: `EventBus` publishes `TaskEvent`s to subscribers
- **Repository**: Abstract data access, swappable persistence


## Highlights
- Demonstrates professional Python patterns: OOP, dataclasses, Observer pattern
- Robust CLI behavior with validation, recovery, and informative messages
- Config management allows runtime customization without editing JSON
- Event-driven architecture for logging task events decoupled from CLI logic
- Fully tested with pytest (fixtures, parametrization, exception testing)
- Uses Rich for a polished terminal experience
- **Modular design**: Loosely-coupled modules enable easy testing and extensions

## Screenshots

To add screenshots to this README:

1. **Main List View** (`python main.py list`)
   - Capture the Rich table showing all tasks with colors
   - Place: After the **Usage** section
   - Description: Shows task display with ID, status, title, type, and extras (due date/priority)

2. **Stats View** (`python main.py stats`)
   - Capture the stats panel showing totals, done count, overdue, and breakdown by type
   - Place: In Features or Usage section
   - Description: Display project statistics

3. **Interactive Mode** (`python main.py interactive`)
   - Capture the arrow-key menu with task selection UI
   - Place: In Features section
   - Description: Shows interactive task management interface

4. **Themes Comparison** 
   - Capture the same list view in different themes (`default`, `minimal`, `dracula`)
   - Place: Near the Customizable themes feature
   - Description: Visual comparison of theme styling
