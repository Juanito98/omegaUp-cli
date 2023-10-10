import click

from commands.add.testvalidator.testvalidator import test_validator


@click.group()
def add() -> None:
    pass


add.add_command(test_validator)
