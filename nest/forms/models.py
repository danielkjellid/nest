from typing import ClassVar

from pydantic import BaseModel


class Form(BaseModel):
    COLUMNS: ClassVar[int] = 1
