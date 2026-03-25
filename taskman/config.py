# Backward compatibility wrapper - imports moved to taskman.config module
from taskman.config.config import Config, ConfigError, CONFIG_PATH
from taskman.config.themes import Theme, THEMES, get_theme

__all__ = ['Config', 'ConfigError', 'CONFIG_PATH', 'Theme', 'THEMES', 'get_theme']
