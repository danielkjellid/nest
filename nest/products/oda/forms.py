from nest.forms.models import Form
from nest.forms.fields import FormField


class ProductOdaImportForm(Form):
    COLUMNS = 1

    oda_product_id: int = FormField(..., help_text="Product Id at Oda.")
