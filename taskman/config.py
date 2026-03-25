from dataclasses import dataclass, fields
from pathlib import Path
import json

CONFIG_PATH = Path.home() / ".taskman" / "config.json"

@dataclass
class Config:
    data_dir: str = str(Path.home() / ".taskman")
    date_format: str = "%Y-%m-%d"
    color_output: bool = True
    default_filter: str = "all"
    theme: str = "default"

    @classmethod
    def load(cls) -> "Config":
        if not CONFIG_PATH.exists():
            return cls()
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        valid_keys = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in valid_keys})

    def save(self) -> None:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(self.__dict__, indent=2), encoding="utf-8")


class ConfigError(Exception):
    pass


def handle_config_set(args, _):
    cfg = Config.load()
    if not args.set:
        print("Please provide --set key=value")
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
    print(f"Config updated: {key} = {val}")