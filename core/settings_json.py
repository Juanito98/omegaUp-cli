import os
import json

from typing import Dict

_KEYS = [
    "title",
    "source",
    "limits",
    "validator",
    "interactive",
    "misc"
]


def get_settings_json(problem_dir: str) -> Dict:
    with open(os.path.join(problem_dir, "settings.json"), "r") as p:
        config: Dict = json.load(p)
    return config


def save_settings_json(problem_dir: str, config: Dict) -> None:
    """Save the problems.json file."""
    # Order by keys
    assert set(config.keys()).issubset(_KEYS)
    config = {k: config[k] for k in _KEYS if k in config}
    with open(os.path.join(problem_dir, "settings.json"), "w") as p:
        json.dump(config, p, indent=2)
        p.write("\n")
