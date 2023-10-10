import os
from typing import Optional
from core.subtasks import infer_number_subtask_from_statements
from core.logging import logging
from core.tests_json import get_tests_json, save_tests_json
from core.problems_json import get_problem_paths
from core.repository import repository_root
import click
import inquirer

from .template import files


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
@click.option(
    "--validator",
    default="test-validator.py",
    help="The validator file name.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing files.",
)
def test_validator(
    root: str,
    path: Optional[str],
    validator: str,
    overwrite: bool,
) -> None:
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

    logging.info(f"Adding test validator to problem {path}...")
    if overwrite:
        logging.info("Overwriting existing files...")

    problem_dir = os.path.join(root, path)

    # Add validator to tests.json
    logging.info("Adding validator to tests.json...")
    test_json = get_tests_json(problem_dir)
    test_json["inputs"] = {"filename": validator}
    save_tests_json(problem_dir, test_json)

    # Infer number of subtasks
    num_subtasks = infer_number_subtask_from_statements(problem_dir)
    subtasks = ""
    if num_subtasks > 0:
        subtasks = (
            "if "
            + "\n        elif ".join(
                [
                    (
                        f"'sub{i}' in caseName:\n            pass"
                        f"  # TODO: Validate subtask {i}"
                    )
                    for i in range(1, num_subtasks + 1)
                ]
            )
            + "\n        else:\n            self.fail(f'Invalid subtask {caseName}')"
        )

    # Add files
    # Create files
    d = {"validator": validator, "subtasks": subtasks}
    for file in files:
        file_path = os.path.join(problem_dir, file["path"].format(**d))
        content = file["content"].format(**d)
        # Checking if file already exists
        if not overwrite and os.path.exists(file_path):
            raise click.ClickException(f"File {file_path} already exists.")
        # Creating directories if necessary
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Creating file
        with open(file_path, "w") as f:
            logging.info(f"Creating file {file_path}...")
            f.write(content)
