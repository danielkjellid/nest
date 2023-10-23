from django.urls import reverse


def test_url_recipe_create_api():
    """
    Test reverse match of the recipe_create endpoint.
    """
    url = reverse("api-1.0.0:recipe_create_api")
    assert url == "/api/v1/recipes/create/"


def test_url_recipe_detail_api():
    """
    Test reverse match of the recipe_detail endpoint.
    """
    url = reverse("api-1.0.0:recipe_detail_api", args=["recipe_id"])
    assert url == "/api/v1/recipes/recipe_id/"


def test_url_recipe_list_api():
    """
    Test reverse match of the recipe_list endpoint.
    """
    url = reverse("api-1.0.0:recipe_list_api")
    assert url == "/api/v1/recipes/"
