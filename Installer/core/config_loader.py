from pathlib import Path

def load_config(path: Path) -> dict[str, list[str]]:
    """
    Simple YAML loader for our config.yaml.
    Only supports:
      key:
        - value
        - value2
    """
    config: dict[str, list[str]] = {}
    current_key: str | None = None

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.endswith(":"):
                current_key = line[:-1].strip()
                config[current_key] = []
            elif line.startswith("- ") and current_key:
                config[current_key].append(line[2:].strip())
            # else ignore invalid lines
    return config
