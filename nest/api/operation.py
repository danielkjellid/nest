"""
This is a hack to add view_func_kwargs to the operation class be able to pass kwargs
to view functions on execution. Specifically used for the sake of form generation
endpoints.
"""
from typing import Any, Callable, Sequence

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from ninja.constants import NOT_SET
from ninja.operation import (
    Operation as NinjaOperation,
)
from ninja.operation import (
    PathView as NinjaPathView,
)
from ninja.signature import is_async


class Operation(NinjaOperation):
    def __init__(
        self,
        path: str,
        methods: list[str],
        view_func: Callable[..., Any],
        *,
        view_func_kwargs: dict[str, Any] | None,
        **kwargs: Any,
    ):
        super().__init__(path, methods, view_func, **kwargs)
        self.view_func_kwargs = view_func_kwargs

    def run(self, request: HttpRequest, **kw: Any) -> HttpResponseBase:
        error = self._run_checks(request)
        if error:
            return error
        try:
            temporal_response = self.api.create_temporal_response(request)
            values = self._get_values(request, kw, temporal_response)
            # Inject kwargs into view func.
            view_kwargs = self.view_func_kwargs or {}
            result = self.view_func(request, **view_kwargs, **values)
            return self._result_to_response(request, result, temporal_response)
        except Exception as e:
            if isinstance(e, TypeError) and "required positional argument" in str(e):
                msg = "Did you fail to use functools.wraps() in a decorator?"
                msg = f"{e.args[0]}: {msg}" if e.args else msg
                e.args = (msg,) + e.args[1:]
            return self.api.on_exception(request, e)


class AsyncOperation(Operation):
    def __init__(
        self, view_func_kwargs: dict[str, Any] | None, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.view_func_kwargs = view_func_kwargs

    async def run(self, request: HttpRequest, **kw: Any) -> HttpResponseBase:  # type: ignore
        error = self._run_checks(request)
        if error:
            return error
        try:
            temporal_response = self.api.create_temporal_response(request)
            values = self._get_values(request, kw, temporal_response)
            # Inject kwargs into view func.
            view_kwargs = self.view_func_kwargs or {}
            result = await self.view_func(request, **view_kwargs, **values)
            return self._result_to_response(request, result, temporal_response)
        except Exception as e:
            return self.api.on_exception(request, e)


class PathView(NinjaPathView):
    def __init__(self) -> None:
        super().__init__()

    def add_operation(
        self,
        path: str,
        methods: list[str],
        view_func: Callable[..., Any],
        *,
        view_func_kwargs: dict[str, Any] | None = None,
        auth: Sequence[Callable[..., Any]]
        | Callable[..., Any]
        | object
        | None = NOT_SET,
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
    ) -> Operation | AsyncOperation:
        if url_name:
            self.url_name = url_name

        OperationClass = Operation

        if is_async(view_func):
            self.is_async = True
            OperationClass = AsyncOperation  # type: ignore

        operation = OperationClass(
            path,
            methods,
            view_func,
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
            include_in_schema=include_in_schema,
            url_name=url_name,
            openapi_extra=openapi_extra,
        )

        self.operations.append(operation)
        return operation
