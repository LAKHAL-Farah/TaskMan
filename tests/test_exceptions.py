import pytest
from taskman.exceptions import (
    TaskManError,
    TaskNotFoundError,
    StorageError,
    ValidationError,
    ConfigError
)

# ----------------------
# Base exception
# ----------------------
def test_taskmanerror_is_base():
    e = TaskManError("Base error")
    assert isinstance(e, Exception)
    assert str(e) == "Base error"

# ----------------------
# TaskNotFoundError
# ----------------------
def test_tasknotfounderror_message():
    e = TaskNotFoundError(task_id=42)
    assert isinstance(e, TaskManError)
    assert e.task_id == 42
    assert str(e) == "No task with id=42"

# ----------------------
# StorageError
# ----------------------
def test_storageerror_message():
    e = StorageError("Cannot read file")
    assert isinstance(e, TaskManError)
    assert str(e) == "Cannot read file"

# ----------------------
# ValidationError
# ----------------------
def test_validationerror_message():
    e = ValidationError("Invalid input")
    assert isinstance(e, TaskManError)
    assert str(e) == "Invalid input"

# ----------------------
# ConfigError
# ----------------------
def test_configerror_message():
    e = ConfigError("Bad config")
    assert isinstance(e, TaskManError)
    assert str(e) == "Bad config"

# ----------------------
# Catching at the top level
# ----------------------
def test_catching_hierarchy():

    for exc_class in [TaskNotFoundError, StorageError, ValidationError, ConfigError]:
        with pytest.raises(TaskManError):
            raise exc_class("test") if exc_class != TaskNotFoundError else exc_class(1)