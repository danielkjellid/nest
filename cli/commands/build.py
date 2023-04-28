import click

from .utils.executables import run_cli_command
from .utils.managers import action_runner


@click.command(help="Build application files")
def build() -> None:
    # Install required dependencies according to pyproject.toml.
    with action_runner(description="Installing poetry dependencies"):
        run_cli_command("poetry", "install", "--no-dev")

    # Collect static files.
    with action_runner(description="Collecting static files"):
        run_cli_command("python", "manage.py", "collectstatic", "--no-input")

    # Migrate database to latest state.
    with action_runner(description="Migrating database"):
        run_cli_command("python", "manage.py", "migrate")
