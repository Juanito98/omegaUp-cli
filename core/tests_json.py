import os
import json
from typing import Dict


def get_tests_json(problem_dir: str) -> Dict:
    with open(os.path.join(problem_dir, "tests/tests.json"), "r") as p:
        config = json.load(p)
    return config


def save_tests_json(problem_dir: str, config: Dict) -> None:
    """Save the problems.json file."""
    # Order config by keys
    config = {k: config[k] for k in sorted(config)}
    with open(os.path.join(problem_dir, "tests/tests.json"), "w") as p:
        json.dump(config, p, indent=2)
        p.write("\n")
