from typing import Optional
from core.problems_json import get_problem_paths
from core.repository import repository_root
import click
import inquirer


@click.command()
@click.option(
    "--root",
    default=repository_root(),
    help="The root directory of the project.",
    type=click.Path(exists=True),
)
@click.option(
    "--path",
    default=None,
    help="The directory name of the problem.",
)
def test_validator(
    root: str,
    path: Optional[str],
):
    if path is None:
        problems = get_problem_paths(root)
        path = str(
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
