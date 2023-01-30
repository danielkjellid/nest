from typing import Any

from sqlalchemy.ext.declarative import declarative_base, declared_attr

from nest.database.utils import resolve_table_name


class CustomBase:
    __repr_attrs__: list[str] = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self) -> str:
        module = self.__module__.rsplit(".")[-1]
        return resolve_table_name(f"{module}{self.__name__}")  # type: ignore

    def dict(self) -> dict[Any, Any]:
        """
        Returns the dict representation of a model.
        """
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns  # type: ignore
        }


Base = declarative_base(cls=CustomBase)
