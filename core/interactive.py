from typing import Tuple
from .problems_json import get_problem_paths
import inquirer


def fetch_problems_dir(root: str) -> str:
    problems = get_problem_paths(root)
    return str(
        inquirer.prompt(
            [
                inquirer.List(
                    "path",
                    message="What is the directory name of the problem?",
                    choices=problems,
                )
            ]
        )["path"]
    )


def fetch_string_text(prompt: str) -> str:
    return str(
        inquirer.prompt(
            [
                inquirer.Text(
                    "text",
                    message=prompt,
                )
            ]
        )["text"]
    )


def fetch_string_editor(prompt: str) -> str:
    return str(
        inquirer.prompt(
            [
                inquirer.Editor(
                    "editor",
                    message=prompt,
                )
            ]
        )["editor"]
    )


def fetch_int_range(prompt: str, min_range: int, max_range: int) -> Tuple[int, int]:
    left = int(
        inquirer.prompt(
            [
                inquirer.Text(
                    "number",
                    message=f"Enter min value for {prompt} ({min_range}-{max_range})",
                    validate=lambda _, x: min_range <= int(x) <= max_range,
                )
            ]
        )["number"]
    )
    right = int(
        inquirer.prompt(
            [
                inquirer.Text(
                    "number",
                    message=f"Enter max value for {prompt} ({min_range}-{max_range})",
                    validate=lambda _, x: left <= int(x) <= max_range,
                )
            ]
        )["number"]
    )
    return left, right
