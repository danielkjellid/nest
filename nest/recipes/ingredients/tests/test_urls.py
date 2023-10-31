from django.urls import reverse


def test_url_recipe_ingredient_create_api():
    """
    Test reverse match of the recipe_ingredient_create_api endpoint.
    """
    url = reverse("api-1.0.0:recipe_ingredient_create_api")
    assert url == "/api/v1/recipes/ingredients/create/"


def test_url_recipe_ingredient_delete_api():
    """
    Test reverse match of the recipe_ingredient_delete_api endpoint.
    """
    url = reverse("api-1.0.0:recipe_ingredient_delete_api")
    assert url == "/api/v1/recipes/ingredients/delete/"


def test_url_recipe_ingredient_list_api():
    """
    Test reverse match of the recipe_ingredient_list_api endpoint.
    """
    url = reverse("api-1.0.0:recipe_ingredient_list_api")
    assert url == "/api/v1/recipes/ingredients/"


def test_url_recipe_ingredient_groups_create_api():
    """
    Test reverse match of the recipe_ingredient_groups_create_api endpoint.
    """
    url = reverse("api-1.0.0:recipe_ingredient_groups_create_api", args=["recipe_id"])
    assert url == "/api/v1/recipes/ingredients/recipe_id/groups/create/"


def test_url_recipe_ingredient_groups_list_api():
    """
    Test reverse match of the recipe_ingredient_groups_list_api endpoint.
    """
    url = reverse("api-1.0.0:recipe_ingredient_groups_list_api", args=["recipe_id"])
    assert url == "/api/v1/recipes/ingredients/recipe_id/groups/"
