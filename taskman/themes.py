# Backward compatibility wrapper - imports moved to taskman.config module
from taskman.config.themes import Theme, THEMES, get_theme

__all__ = ['Theme', 'THEMES', 'get_theme']
