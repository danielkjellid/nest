from pydantic import BaseModel


class TableRecord(BaseModel):
    key: str
    parent_key: str | None = None
    title: str
    value: str
