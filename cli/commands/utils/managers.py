import contextlib
import subprocess
import sys
from typing import Iterator, Optional

import click

from .colors import gray, red
from .helpers import print_with_time


class Cancel(RuntimeError):
    def __init__(self, *, description: str, help: str = "") -> None:
        super().__init__()
        self.description = description
        self.help = help


@contextlib.contextmanager
def action_runner(
    *,
    description: str,
    exit_on_failure: bool = True,
    error_message: Optional[str] = None,
) -> Iterator[None]:
    """
    A context manager that handles subprocess errors.
    """

    print_with_time(gray(f"{description}... "), end="", flush=True)

    try:
        yield
        click.echo("✅")
    except subprocess.CalledProcessError as e:
        click.echo("❌")
        click.echo(
            red(
                f"An error occured while running "
                f'"{" ".join(str(arg) for arg in e.args)}"'
            )
        )

        if e.stdout:
            click.echo("-" * 20 + red(" stdout ") + "-" * 20)
            click.echo(e.stdout.strip())
            click.echo("-" * 48)

        if e.stderr:
            click.echo("-" * 20 + red(" stderr ") + "-" * 20)
            click.echo(e.stderr.strip())
            click.echo("-" * 48)

        if not exit_on_failure:
            raise

        if error_message:
            sys.exit(error_message)

        sys.exit(1)

    except Cancel as e:
        click.echo("❌")
        click.echo(red(e.description))

        if e.help:
            click.echo(e.help)

        if not exit_on_failure:
            raise

        sys.exit(1)
