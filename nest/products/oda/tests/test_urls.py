from django.urls import reverse


def test_url_product_oda_import_api():
    """
    Test reverse match of the product_oda_import_api endpoint.
    """
    url = reverse("api-1.0.0:product_oda_import_api")
    assert url == "/api/v1/products/oda/import/"


def test_url_product_oda_import_confirm_api():
    """
    Test reverse match of the product_oda_import_confirm_api endpoint.
    """
    url = reverse("api-1.0.0:product_oda_import_confirm_api")
    assert url == "/api/v1/products/oda/import/confirm/"
