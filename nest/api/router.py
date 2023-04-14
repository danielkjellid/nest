from ninja import Router as NinjaRouter, Schema
from typing import Any, TypeVar
from nest.forms.api_view import form_api
from nest.forms.records import FormRecord
from nest.api.responses import APIResponse
from typing import Callable
from ninja.constants import NOT_SET
from .operation import PathView
import structlog

logger = structlog.getLogger()

S = TypeVar("S", bound=Schema)


class Router(NinjaRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_form(self, path, form: S):
        def decorator(func: Any):
            self.add_api_operation(
                path,
                ["GET"],
                view_func=form_api,
                view_func_kwargs={"form": form},
                response={200: APIResponse[FormRecord[form]]},
                summary=f"Generated form for payload {form.__name__}",
            )

            return form_api

        return decorator

    def add_api_operation(
        self,
        path: str,
        methods: list[str],
        view_func: Callable,
        *,
        view_func_kwargs: Any | None = None,
        auth: Any = NOT_SET,
        response: Any = NOT_SET,
        operation_id: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: str | None = None,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> None:
        if path not in self.path_operations:
            path_view = PathView()
            self.path_operations[path] = path_view
        else:
            path_view = self.path_operations[path]

        path_view.add_operation(
            path=path,
            methods=methods,
            view_func=view_func,
            view_func_kwargs=view_func_kwargs,
            auth=auth,
            response=response,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )
        if self.api:
            path_view.set_api_instance(self.api, self)

        return None
