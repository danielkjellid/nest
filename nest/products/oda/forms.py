from typing import ClassVar

from nest.forms.fields import FormField
from nest.forms.models import Form


class ProductOdaImportForm(Form):
    COLUMNS: ClassVar[int] = 1

    oda_product_id: int = FormField(..., help_text="Product Id at Oda.")
