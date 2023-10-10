import os
from typing import Dict, Optional
from core.tests_json import get_tests_json, save_tests_json
from core.logging import logging
from core.interactive import (
    fetch_int_range,
    fetch_problems_dir,
)
from core.repository import repository_root
from .template import files, official_solution_files, cpp_template
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
    "--name",
    prompt=True,
    default="solution.cpp",
    help="The name of the solution file.",
    callback=lambda ctx, param, x: x if "." in x else x + ".cpp",
)
@click.option(
    "--verdict",
    prompt=True,
    default="AC",
    help="The verdict of the solution.",
    type=click.Choice(["AC", "WA", "PA", "TLE", "RTE", "MLE", "CE", "IE"]),
)
@click.option(
    "--disable-official-solution",
    is_flag=True,
    default=False,
    help="Disable official solution.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing files.",
)
def solution(
    root: str,
    path: Optional[str],
    name: str,
    verdict: str,
    disable_official_solution: bool,
    overwrite: bool,
) -> None:
    if path is None:
        path = fetch_problems_dir(root)

    problem_dir = os.path.join(root, path)

    logging.info(f"Adding solution to problem {path}...")
    if overwrite:
        logging.info("Overwriting existing files...")

    # Add solution to tests.json
    logging.info("Adding solution to tests.json...")
    test_json = get_tests_json(problem_dir)
    if "solutions" not in test_json:
        test_json["solutions"] = []
    if any(solution["filename"].endswith(name) for solution in test_json["solutions"]):
        if not overwrite:
            raise click.ClickException(f"Solution {name} already exists.")
        # Remove it if it already exists
        test_json["solutions"] = [
            solution
            for solution in test_json["solutions"]
            if not solution["filename"].endswith(name)
        ]
    payload: Dict = {
        "filename": name,
        "verdict": verdict,
    }
    if verdict != "AC":
        # Get score_range
        min_score, max_score = fetch_int_range("score", 0, 100)
        payload["score_range"] = [min_score / 100, max_score / 100]
    test_json["solutions"].append(payload)
    save_tests_json(problem_dir, test_json)

    # Template parameters
    template = cpp_template if name.endswith(".cpp") else ""
    use_official_solution = (
        name.startswith("solution.") and not disable_official_solution
    )
    solution_files = files
    if use_official_solution:
        solution_files += official_solution_files

    # Create files
    d = {
        "case_name": name,
        "case_template": template,
    }
    for file in solution_files:
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

    if use_official_solution:
        logging.info("Removing .outs cases...")
        # Read all cases and remove .out files
        dirs = ["cases", "examples"]
        for dir in dirs:
            cases = [
                f
                for f in os.listdir(os.path.join(problem_dir, dir))
                if f.endswith(".out")
            ]
            for case in cases:
                case_path = os.path.join(problem_dir, dir, case)
                logging.info(f"Removing {case_path}...")
                os.remove(case_path)
