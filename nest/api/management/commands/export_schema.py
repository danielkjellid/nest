import json
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from nest.api.v1 import api


class Command(BaseCommand):
    help = "Export OpenAPI Schema"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--output", dest="output", default=None, type=str)

    def handle(self, *args: Any, **options: Any) -> None:
        schema = api.get_openapi_schema()
        result = json.dumps(schema, indent=4, sort_keys=False)

        if options["output"]:
            with open(options["output"], "wb") as f:
                f.write(result.encode())
        else:
            self.stdout.write(result)
