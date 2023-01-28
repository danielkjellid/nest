import os

import click
import uvicorn

from nest import config


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "staging", "prod"], case_sensitive=False),
    default="local",
)
@click.option("--debug", type=click.BOOL, is_flag=True, default=False)
def main(env: str, debug: bool) -> None:
    os.environ["ENVIRONMENT"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="app:app",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
