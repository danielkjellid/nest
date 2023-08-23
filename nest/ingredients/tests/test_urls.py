from django.urls import reverse


class TestIngredientsUrls:
    def test_url_ingredient_list_api(self):
        """
        Test reverse match of the ingredient_list_api endpoint.
        """
        url = reverse("api-1.0.0:ingredient_list_api")
        assert url == "/api/v1/ingredients/"

    def test_url_ingredient_create_api(self):
        """
        Test reverse match of the ingredient_create_api endpoint.
        """
        url = reverse("api-1.0.0:ingredient_create_api")
        assert url == "/api/v1/ingredients/create/"
