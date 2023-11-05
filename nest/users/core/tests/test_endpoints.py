import pytest

from store_kit.http import status
from nest.users.core.endpoints import user_list_api

pytestmark = pytest.mark.django_db


class TestEndpointUsersList:
    ENDPOINT = "/api/v1/users/"

    def test_anonymous_request_user_list_api(
        self, django_assert_num_queries, anonymous_client_fixture, mocker
    ):
        """
        Test that unauthenticated users gets a 401 unauthorized on retrieving the user
        list.
        """

        client = anonymous_client_fixture
        selector_mock = mocker.patch(f"{user_list_api.__module__}.get_users")

        with django_assert_num_queries(0):
            response = client.get(self.ENDPOINT)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert selector_mock.call_count == 0

    def test_staff_request_user_list_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that authenticated users gets a valid response.
        """

        client = authenticated_staff_client
        selector_mock = mocker.patch(f"{user_list_api.__module__}.get_users")

        with django_assert_num_queries(2):
            response = client.get(self.ENDPOINT)

        assert response.status_code == status.HTTP_200_OK
        assert selector_mock.call_count == 1
