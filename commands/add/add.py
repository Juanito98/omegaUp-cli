from commands.add.interactive.interactive import interactive
from commands.add.solution.solution import solution
from commands.add.invalidcase.invalidcase import invalid_case
import click

from commands.add.testvalidator.testvalidator import test_validator


@click.group()
def add() -> None:
    pass


add.add_command(test_validator)
add.add_command(invalid_case)
add.add_command(solution)
add.add_command(interactive)
