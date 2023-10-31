from django.urls import reverse


def test_url_product_list_api():
    """
    Test reverse match of the product_list_api endpoint.
    """
    url = reverse("api-1.0.0:product_list_api")
    assert url == "/api/v1/products/"


def test_url_product_create_api():
    """
    Test reverse match of the product_create_api endpoint.
    """
    url = reverse("api-1.0.0:product_create_api")
    assert url == "/api/v1/products/create/"


def test_url_product_detail_api():
    """
    Test reverse match of the product_detail_api endpoint.
    """
    url = reverse("api-1.0.0:product_detail_api", args=["product_id"])
    assert url == "/api/v1/products/product_id/"


def test_url_product_edit_api():
    """
    Test reverse match of the product_edit_api endpoint.
    """
    url = reverse("api-1.0.0:product_edit_api", args=["product_id"])
    assert url == "/api/v1/products/product_id/edit/"
