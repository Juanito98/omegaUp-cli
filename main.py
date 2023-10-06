#!python3
from core.logging import init_logger
import click

from commands.new import new


@click.group()
def ofmi_cli() -> None:
    pass


def main() -> None:
    init_logger()
    ofmi_cli.add_command(new)
    ofmi_cli()


if __name__ == "__main__":
    main()
