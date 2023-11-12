import json
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from nest.forms import forms


class Command(BaseCommand):
    help = "Export forms Schema"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--output", dest="output", default=None, type=str)

    def handle(self, *args: Any, **options: Any) -> None:
        schema = forms.generate_schema()
        result = json.dumps(schema, indent=4, sort_keys=False)

        if options["output"]:
            with open(options["output"], "wb") as f:
                f.write(result.encode())
        else:
            self.stdout.write(result)
