from ninja import Router as NinjaRouter, Schema
from typing import Any, TypeVar
from nest.forms.api_view import form_api
from nest.forms.records import FormRecord
import functools
import structlog

logger = structlog.getLogger()

S = TypeVar("S", bound=Schema)


class Router(NinjaRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_form(self, path, form: S):
        print("Called 1")
        logger.info("EEEEYYYY")

        def decorator(func: Any):
            self.add_api_operation(
                path,
                ["GET"],
                view_func=form_api,
                response={200: FormRecord},
            )
            # print(func)
            # print(func)
            # print(kwargs)
            # setattr(form_api, "test", form)
            # print(form_api.__getattribute__("test"))
            # *arg, request = args
            return form_api

        return decorator
