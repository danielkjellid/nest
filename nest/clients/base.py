import functools
import threading
import uuid
from typing import Any, ClassVar, Type, TypeVar

import requests
import structlog
from pydantic import BaseModel
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

T_BASE_MODEL = TypeVar("T_BASE_MODEL", bound=BaseModel)

logger = structlog.getLogger()
init_lock = threading.Lock()
threadlocal = threading.local()


class BaseHTTPClient:
    name: str = "base"

    # Authentication
    auth_token_prefix: str | None = "Token"
    auth_token: str | None = None

    # Meta
    enabled: bool = False
    request_timeout = (5.0, 20.0)  # (Connect timeout, Read timeout).

    # Url prepended to all calls.
    base_url: str

    _thread_prop: ClassVar[str | None]

    class RequestError(RuntimeError):
        """
        Exception raised if an API call fails, and we should not retry the request.
        """

        def __init__(self, *, status_code: int, body: Any) -> None:
            super().__init__(status_code, body)

        @property
        def status_code(self) -> Any:
            return self.args[0]

        @property
        def body(self) -> Any:
            return self.args[1]

    def __init__(self) -> None:
        if self._thread_prop and hasattr(threadlocal, self._thread_prop):
            raise RuntimeError(
                f"Only a sungle instance of {self.name} should exist per thread."
            )

        if self.enabled and (not self.base_url or self.base_url[-1] == "/"):
            raise ValueError(
                f"Base URL cannot end with a /. Base URL was {self.base_url}"
            )

        self._session = requests.Session()

    @classmethod
    def init(cls) -> Any:
        """
        Create a singleton instance.
        """

        with init_lock:
            if not hasattr(cls, "_thread_prop"):
                cls._thread_prop = str(uuid.uuid4())

            assert cls._thread_prop

            if hasattr(threadlocal, cls._thread_prop):
                return getattr(threadlocal, cls._thread_prop)

            instance = cls()
            setattr(threadlocal, cls._thread_prop, instance)

        return instance

    @classmethod
    def clear(cls) -> None:
        """
        Delete the singleton instance.
        """

        if hasattr(cls, "_thread_prop"):
            assert cls._thread_prop

            if hasattr(threadlocal, cls._thread_prop):
                delattr(threadlocal, cls._thread_prop)

            delattr(cls, "_thread_prop")

    @classmethod
    def serialize_response(
        cls, serializer_cls: Type[T_BASE_MODEL], response: Response | None
    ) -> T_BASE_MODEL:
        """
        Performs the mundane task of verifying that the response retrieved adders to
        the expected structure, raising a pydantic.error_wrappers.ValidationError if it
        doesn't, that the model populated with data if it does.
        """
        print(response)
        print(type(response))
        serializer: T_BASE_MODEL = serializer_cls(**response.json() if response else {})
        return serializer

    def parse_response_error(self, *, response: Response) -> None:
        """
        Override this method to implement a custom response parser. This can be used
        to raise a more detailed exception than the one recieved from the response.
        """

        raise NotImplementedError()

    def get_auth_token(self) -> str | None:
        return self.auth_token

    @classmethod
    def _request(
        cls,
        url: str,
        *,
        method: str,
        params: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: tuple[float, float] | None = None,
        status_codes: tuple[int, ...] | None = None,
    ) -> Response | None:
        """
        Make a request with a given method and parameters.
        """

        instance = cls.init()

        if url[0] != "/":
            raise ValueError(f"Request URL must start with a /, but the URL was: {url}")

        if headers is None:
            headers = {}

        if status_codes is None:
            status_codes = tuple(range(200, 300))

        if cls.auth_token_prefix is not None:
            # Add auth token to request.
            auth_token = instance.get_auth_token()
            if auth_token:
                headers.update(
                    {"Authorization": f"{instance.auth_token_prefix} {auth_token}"}
                )

        if not instance.enabled:
            logger.warning(
                "Faking HTTP request",
                name=instance.name,
                method=method,
                url=url,
                params=params,
                headers=headers,
                data=data,
                json=json,
            )
            return None

        url = f"{instance.base_url}{url}"
        session = cls.create_retry_session(session=instance._session)
        response = session.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            data=data,
            json=json,
            timeout=timeout if timeout is not None else instance.request_timeout,
            allow_redirects=False,
        )

        if response.status_code not in status_codes:
            try:
                instance.parse_response_error(response=response)
            except NotImplementedError:
                pass

            raise instance.RequestError(
                status_code=response.status_code, body=response.text
            )

        return response

    get = functools.partialmethod(_request, method="GET")
    post = functools.partialmethod(_request, method="POST")
    put = functools.partialmethod(_request, method="PUT")
    patch = functools.partialmethod(_request, method="PATCH")
    delete = functools.partialmethod(_request, method="DELETE")

    @classmethod
    def create_retry_session(
        cls,
        session: Session | None,
        retries: int = 1,
        backoff: float = 0.4,
        status_forcelist: tuple[int, ...] = (502, 503, 504),
    ) -> Session:
        """
        Retry on connection failures and bad status codes.
        """

        session = session or Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session
