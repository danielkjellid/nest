from django.urls import reverse


def test_url_recipe_steps_create_api():
    """
    Test reverse match of the recipe_steps_create_api endpoint.
    """
    url = reverse("api-1.0.0:recipe_steps_create_api", args=["recipe_id"])
    assert url == "/api/v1/recipes/steps/recipe_id/create/"
