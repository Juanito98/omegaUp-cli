import click
import os
import logging
import datetime

from .template import files, symlinks
from core.repository import repository_root
from core.problems_json import get_problems_json, save_problems_json


@click.command()
@click.option(
    "--root",
    default=repository_root(),
    help="The root directory of the project.",
    type=click.Path(exists=True),
)
@click.option(
    "--path",
    prompt=True,
    help="The directory name of the problem.",
)
@click.option(
    "--title",
    prompt=True,
    default="<title>",
    help="The title of the problem.",
)
@click.option(
    "--source",
    prompt=True,
    default="<source>",
    help="The source of the problem.",
)
@click.option(
    "--admin-group",
    prompt=True,
    default=f"ofmi-{datetime.date.today().year}",
    help="The admin group for the problem.",
)
@click.option(
    "--alias",
    prompt=True,
    default="dummy-ofmi",
    help="The alias for the problem.",
)
@click.option(
    "--sample",
    default="sample",
    help="The example file name.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing files.",
)
def problem(
    root: str,
    path: str,
    title: str,
    source: str,
    admin_group: str,
    alias: str,
    sample: str,
    overwrite: bool,
) -> None:
    logging.info(f"Creating problem {path}...")
    if overwrite:
        logging.info("Overwriting existing files...")
    config = get_problems_json(root)

    # Add problem to problems.json
    problem_paths = [problem["path"] for problem in config["problems"]]
    if not overwrite and path in problem_paths:
        raise click.ClickException(f"Problem {path} already exists.")
    else:
        logging.info(f"Adding problem {path} to problems.json...")
        config["problems"].append(
            {
                "path": path,
            }
        )
        save_problems_json(root, config)

    # Create problem directory
    if not overwrite and os.path.exists(os.path.join(root, path)):
        raise click.ClickException(f"Directory {path} already exists.")
    os.makedirs(os.path.join(root, path), exist_ok=True)

    # Create files
    d = {
        "title": title,
        "source": source,
        "sample": sample,
        "admin_group": admin_group,
        "alias": alias,
    }
    for file in files:
        file_path = os.path.join(root, path, file["path"].format(**d))
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

    # Creating symlink
    for symlink in symlinks:
        src = os.path.join(root, path, symlink["src"].format(**d))
        if not os.path.exists(src):
            raise click.ClickException(f"Symlink source {src} does not exist.")
        dst = os.path.join(root, path, symlink["dst"].format(**d))
        # Checking if symlink already exists
        if os.path.exists(dst):
            if not overwrite:
                raise click.ClickException(f"Symlink {dst} already exists.")
            else:
                os.remove(dst)
        # Creating directories if necessary
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        # Creating symlink
        logging.info(f"Creating symlink {dst}...")
        src_rel = os.path.relpath(src, os.path.dirname(dst))
        os.symlink(src_rel, dst)
