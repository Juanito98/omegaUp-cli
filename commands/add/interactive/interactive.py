from typing import Optional
from core.subtasks import infer_number_subtask_from_statements
from core.logging import logging
from core.repository import repository_root
from core.settings_json import get_settings_json, save_settings_json
from core.interactive import fetch_problems_dir, fetch_string_text

from .template import settings_json_dict, files, subcase_main, no_subcase_main, symlinks

import click
import os


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
    "--module-name",
    default=None,
    help="The interactive module name.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing files.",
)
def interactive(
    root: str,
    path: Optional[str],
    module_name: Optional[str],
    overwrite: bool,
) -> None:
    if path is None:
        path = fetch_problems_dir(root)

    if module_name is None:
        module_name = fetch_string_text("interactive module name", path)

    logging.info(f"Adding interactive to problem {path}...")
    if overwrite:
        logging.warning("Overwriting existing files...")

    problem_dir = os.path.join(root, path)

    # Agregar interactive section to settings.json
    logging.info("Adding interactive section to settings.json...")
    settings_json = get_settings_json(problem_dir)
    settings_json.update(settings_json_dict)
    settings_json["interactive"]["ModuleName"] = module_name
    save_settings_json(problem_dir, settings_json)

    # Infer number of subtasks
    num_subtasks = infer_number_subtask_from_statements(problem_dir)
    if num_subtasks > 0:
        subtask_content = subcase_main.format(num_sub=num_subtasks)
    else:
        subtask_content = no_subcase_main
    
    # Agregar archivos
    logging.info("Adding files...")
    d = {
        "module_name": module_name,
        "subtasks": subtask_content,
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
        # Creating symlink
        logging.info(f"Creating symlink {dst}...")
        src_rel = os.path.relpath(src, os.path.dirname(dst))
        os.symlink(src_rel, dst)
