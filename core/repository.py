import subprocess


def repositoryRoot() -> str:
    """Returns the root directory of the project.

    If this is a submodule, it gets the root of the top-level working tree.
    """
    return (
        subprocess.check_output(
            ["git", "rev-parse", "--show-superproject-working-tree", "--show-toplevel"],
            universal_newlines=True,
        )
        .strip()
        .split()[0]
    )
