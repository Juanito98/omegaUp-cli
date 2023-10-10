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
