import inspect
from typing import Any, Callable, Type, TypeVar, get_type_hints

import structlog
from ninja import Router as NinjaRouter
from ninja import Schema
from ninja.constants import NOT_SET

from nest.api.responses import APIResponse
from pydantic import create_model
from nest.forms.api_view import form_api
from nest.forms.records import FormRecord
from nest.core.files import UploadedFile, UploadedImageFile

from .operation import PathView

logger = structlog.getLogger()

S = TypeVar("S", bound=Type[Schema])


class Router(NinjaRouter):
    def __init__(self, *, auth: Any = NOT_SET, tags: list[str] | None = None) -> None:
        super().__init__(auth=auth, tags=tags)
        self.path_operations: dict[str, PathView] = {}  # type: ignore

    def add_form(
        self,
        path: str,
        form: S,
        is_multipart_form: bool = False,
        columns: int | None = 1,
    ) -> Callable[..., Callable[..., Any]]:
        def decorator(func: Any) -> Callable[..., Any]:
            # endpoint_type_hints = get_type_hints(func).items()
            # additional_form_fields = {}

            # s = form
            #
            # for key, value in endpoint_type_hints:
            #     if issubclass(value, UploadedFile):
            #         additional_form_fields[key] = (UploadedFile, ...)
            #
            #     if issubclass(value, UploadedImageFile):
            #         additional_form_fields[key] = (UploadedImageFile, ...)
            #
            # form_model = create_model(
            #     form.__name__,
            #     __base__=form,
            #     **{key: value for key, value in additional_form_fields.items()},
            # )

            self.add_api_operation(
                path,
                ["GET"],
                view_func=form_api,
                view_func_kwargs={
                    "form": form,
                    "is_multipart_form": is_multipart_form,
                    "columns": columns,
                },
                response={200: APIResponse[FormRecord]},
                summary=f"Generated form for payload {form.__name__}",
            )

            return form_api

        return decorator

    def add_api_operation(
        self,
        path: str,
        methods: list[str],
        view_func: Callable[..., Any],
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
