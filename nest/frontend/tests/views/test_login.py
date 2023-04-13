from unittest.mock import ANY

from django.test import Client
from django.urls import reverse


class TestViewLogin:
    path = reverse("login")

    def test_login_view_url(self) -> None:
        url = self.path
        assert url == "/login/"

    def test_login_view_accessible(self) -> None:
        """
        Test that the login view is accessible to all users.
        """

        client = Client(enforce_csrf_checks=True)
        response = client.get(self.path, follow=True)

        assert response.status_code == 200

    def test_login_view_context(self) -> None:
        """
        Test that part of the context return is as expected.
        """
        client = Client(enforce_csrf_checks=True)
        response = client.get(self.path, follow=True)

        context_dict = {}
        expected_partial = {
            "DJANGO_VITE_DEV_MODE": ANY,
            "DJANGO_VITE_DEV_SERVER_HOST": ANY,
            "DJANGO_VITE_DEV_SERVER_PORT": ANY,
            "FRONTEND_APP": "frontend/apps/login/index.tsx",
            "form": ANY,
            "csrf_token": ANY,
        }

        # Extract and flatten context properties.
        for subcontext in response.context:
            for d in subcontext.dicts:
                context_dict.update(d)

        assert expected_partial.items() <= context_dict.items()
