from dataclasses import dataclass

@dataclass
class Theme:
    name: str
    done_color: str = "green"
    pending_color: str = "white"
    overdue_color: str = "red"
    header_color: str = "bold purple"
    border_style: str = "ROUNDED"
    priority_color: str = "magenta"


# Define all themes
THEMES = {
    'default': Theme('default'),
    'minimal': Theme('minimal', done_color='', pending_color='', overdue_color=''),
    'dracula': Theme('dracula', done_color='bright_green', header_color='bold magenta'),
}



def get_theme(config) -> Theme:
    return THEMES.get(getattr(config, 'theme', None), THEMES['default'])