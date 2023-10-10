import os
from typing import Optional
from core.logging import logging
from core.interactive import fetch_problems_dir, fetch_string_editor, fetch_string_text
from core.repository import repository_root
from .template import files
import click


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
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing files.",
)
def invalid_case(
    root: str,
    path: Optional[str],
    overwrite: bool,
) -> None:
    if path is None:
        path = fetch_problems_dir(root)

    problem_dir = os.path.join(root, path)

    logging.info(f"Adding invalid case to problem {path}...")
    if overwrite:
        logging.info("Overwriting existing files...")

    case_name = fetch_string_text("Enter the case name")
    invalid_case = fetch_string_editor("Enter the invalid case")
    expected_failure = fetch_string_editor("Enter the expected failure")

    # Create files
    d = {
        "case_name": case_name,
        "invalid_case": invalid_case,
        "expected_failure": expected_failure,
    }
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
