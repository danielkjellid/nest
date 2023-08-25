from django.urls import reverse


class TestRecipeUrls:
    def test_url_recipe_create_api(self):
        """
        Test reverse match of the recipe_create endpoint.
        """
        url = reverse("api-1.0.0:recipe_create_api")
        assert url == "/api/v1/recipes/create/"

    def test_url_recipe_ingredient_groups_create_api(self):
        """
        Test reverse match of the recipe_ingredient_groups_create endpoint.
        """
        url = reverse(
            "api-1.0.0:recipe_ingredient_groups_create_api", args=["recipe_id"]
        )
        assert url == "/api/v1/recipes/recipe_id/ingredient-groups/create/"

    def test_url_recipe_ingredient_group_list_api(self):
        """
        Test reverse match of the recipe_ingredient_groups_list endpoint.
        """
        url = reverse("api-1.0.0:recipe_ingredient_groups_list_api", args=["recipe_id"])
        assert url == "/api/v1/recipes/recipe_id/ingredient-groups/"

    def test_url_recipe_list_api(self):
        """
        Test reverse match of the recipe_list endpoint.
        """
        url = reverse("api-1.0.0:recipe_list_api")
        assert url == "/api/v1/recipes/"

    def test_url_recipe_steps_create_api(self):
        """
        Test reverse match of the recipe_steps_create endpoint.
        """
        url = reverse("api-1.0.0:recipe_steps_create_api", args=["recipe_id"])
        assert url == "/api/v1/recipes/recipe_id/steps/create/"
