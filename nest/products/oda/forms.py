from typing import ClassVar

from pydantic import BaseModel

from nest.api.openapi import form
from nest.core.fields import FormField


@form
class ProductOdaImportForm(BaseModel):
    COLUMNS: ClassVar[int] = 1

    oda_product_id: str = FormField(..., help_text="Product Id at Oda.")
