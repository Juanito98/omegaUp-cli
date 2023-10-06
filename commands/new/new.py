import click

from commands.new.problem import problem


@click.group()
def new() -> None:
    pass


new.add_command(problem)
