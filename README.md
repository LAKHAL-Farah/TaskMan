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
```
## Architecture
| File | Responsibility |
|------|----------------|
| models.py | Task, DeadlineTask, PriorityTask classes |
| storage.py | JSON load/save (only file touching disk) |
| themes.py | Theme definitions, default and custom themes |
| cli.py | argparse setup, command handlers, Rich tables, interactive mode |
| main.py | Entry point |
| tests/ | Unit tests for tasks and functionality |


## Highlights
- Demonstrates professional Python patterns: OOP, error boundaries, idempotency
- Shows robust CLI behavior with validation, recovery, and informative messages
- Includes automated recovery system for corrupted JSON files
- Uses Rich for a polished terminal experience
- Fully tested with pytest (fixtures, parametrization, exception testing)