from nest.forms.fields import FormField
from nest.forms.models import Form


class ProductOdaImportForm(Form):
    COLUMNS = 1

    oda_product_id: int = FormField(..., help_text="Product Id at Oda.")
