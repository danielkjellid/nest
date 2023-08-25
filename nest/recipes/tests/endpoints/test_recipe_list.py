import pytest
from django.urls import reverse
from nest.recipes.endpoints.recipe_list import recipe_list_api

pytestmark = pytest.mark.django_db


class TestEndpointRecipeList:
    ENDPOINT = reverse("api-1.0.0:recipe_list_api")

    def test_anonymous_request_recipe_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users successfully can list recipes.
        """

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{recipe_list_api.__module__}.get_recipes", return_value=[]
        )

        with django_assert_num_queries(2):
            response = client.get(self.ENDPOINT, content_type="application/json")

        assert response.status_code == 200
        assert selector_mock.call_count == 1
