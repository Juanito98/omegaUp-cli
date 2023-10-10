from commands.add.invalidcase.invalidcase import invalid_case
import click

from commands.add.testvalidator.testvalidator import test_validator


@click.group()
def add() -> None:
    pass


add.add_command(test_validator)
add.add_command(invalid_case)
