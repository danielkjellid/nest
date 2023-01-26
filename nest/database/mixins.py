from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    @staticmethod
    @declared_attr
    def created_at():
        return Column(DateTime, default=func.now(), nullable=False)

    @staticmethod
    @declared_attr
    def updated_at():
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
