from unittest.mock import ANY

from django.test import Client
from django.urls import reverse


class TestViewFrontend:
    path = reverse("index")

    def test_frontend_view_restricted(self, unprivileged_user) -> None:
        """
        Test that the frontend view is only accessible to authenticated users.
        """

        user = unprivileged_user
        client = Client(enforce_csrf_checks=True)
        response = client.get(self.path, follow=True)

        assert response.status_code == 200
        assert response.redirect_chain == [("/login/?next=/", 302)]

        # Retry after logging in.
        client.login(username=user.email, password="supersecretpassword")
        res = client.get(self.path, follow=True)

        assert res.status_code == 200
        assert res.redirect_chain == []  # Redirect chain should now be [].

    def test_frontend_view_context(self, unprivileged_user) -> None:
        """
        Test that part of the context return is as expected.
        """

        user = unprivileged_user
        client = Client(enforce_csrf_checks=True)
        client.login(username=user.email, password="supersecretpassword")
        response = client.get(self.path, follow=True)

        context_dict = {}
        expected_partial = {
            "DJANGO_VITE_DEV_MODE": ANY,
            "DJANGO_VITE_DEV_SERVER_HOST": ANY,
            "DJANGO_VITE_DEV_SERVER_PORT": ANY,
            "FRONTEND_APP": "frontend/apps/index.tsx",
            "initial_props": ANY,  # Value is tested in selector.
        }

        # Extract and flatten context properties.
        for subcontext in response.context:
            for d in subcontext.dicts:
                context_dict.update(d)

        assert expected_partial.items() <= context_dict.items()
