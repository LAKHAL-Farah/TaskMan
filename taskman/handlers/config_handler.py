from rich.console import Console
from taskman.config import Config, ConfigError

console = Console()

def handle_config_set(args, _):
    cfg = Config.load()
    if not args.set:
        console.print("[yellow]Please provide --set key=value[/]")
        return
    if "=" not in args.set:
        raise ConfigError("Invalid format, use key=value")
    key, val = args.set.split("=", 1)
    if not hasattr(cfg, key):
        raise ConfigError(f"Unknown config key: {key}")
    if getattr(cfg, key) is True or getattr(cfg, key) is False:
        val = val.lower() in ("true", "1", "yes")
    setattr(cfg, key, val)
    cfg.save()
    console.print(f"[green]Config updated: {key} = {val}[/]")
