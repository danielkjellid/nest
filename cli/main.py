import click

from .commands import build


@click.group()
def cli() -> None:
    ...


cli.add_command(build.build)
