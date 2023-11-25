from typing import ClassVar

from nest.forms.fields import FormField
from nest.forms.models import Form
from nest.api.openapi import form
from pydantic import BaseModel


@form
class ProductOdaImportForm(BaseModel):
    COLUMNS: ClassVar[int] = 1

    oda_product_id: str = FormField(..., help_text="Product Id at Oda.")
