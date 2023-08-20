import pytest
from nest.ingredients.endpoints.ingredient_list import ingredient_list_api
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestEndpointIngredientList:
    ENDPOINT = reverse("api-1.0.0:ingredient_list_api")

    def test_anonymous_request_ingredient_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users are able to retrieve a list of
        ingredients.
        """

        client = authenticated_client
        service_mock = mocker.patch(f"{ingredient_list_api.__module__}.get_ingredients")

        with django_assert_num_queries(2):
            response = client.get(self.ENDPOINT, content_type="application/json")

        assert response.status_code == 200
        assert service_mock.call_count == 1
