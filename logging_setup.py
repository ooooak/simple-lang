import json
import logging
from logging import config
from pathlib import Path


def setup_logging(path: str = "logging.json", default_level=logging.INFO):
    path = Path(path)
    if path.is_file():
        with path.open("r") as f:
            cfg = json.load(f)
        config.dictConfig(cfg)
    else:
        # Fallback: basic config
        logging.basicConfig(level=default_level)
        logging.warning(f"Logging config file not found: {path}. Using basicConfig().")


# Setup logging
setup_logging()