from typing import Any

from sqlalchemy.ext.declarative import declarative_base, declared_attr

from nest.database.utils import resolve_table_name


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)

    def dict(self) -> dict[Any, Any]:
        """
        Returns the dict representation of a model.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=CustomBase)
