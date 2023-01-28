import re
from contextvars import ContextVar, Token

_session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return _session_context.get()


def set_session_context(session_id: str) -> Token[str]:
    return _session_context.set(session_id)


def reset_session_context(context: Token[str]) -> None:
    _session_context.reset(context)


def resolve_table_name(name: str) -> str:
    """
    Resolves table names into their mapped names.
    """
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])
