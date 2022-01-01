from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).parent
config_path = CONFIG_DIR / "main.yaml"


def get_config(path: Path = config_path):
    """Get yaml configuration variables as one config dictionary.

    Args:
        path (Path, optional): Custom path. Defaults to config_path.
    """
    with open(path) as f:
        config = yaml.safe_load(f)
    return config
