import os
import json
from typing import Dict, List


def get_problems_json(repositoryRoot: str) -> Dict:
    with open(os.path.join(repositoryRoot, "problems.json"), "r") as p:
        config = json.load(p)
    return config


def save_problems_json(repositoryRoot: str, config: Dict) -> None:
    """Save the problems.json file."""
    with open(os.path.join(repositoryRoot, "problems.json"), "w") as p:
        json.dump(config, p, indent=2)
        p.write("\n")


def get_problem_paths(repository_root: str) -> List[str]:
    """Get the paths of all the problems."""
    config = get_problems_json(repository_root)
    return [d["path"] for d in config["problems"]]
