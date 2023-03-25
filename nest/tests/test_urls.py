from django.urls import reverse


class TestUrls:
    def test_url_index(self) -> None:
        """
        Test reverse match of index view.
        """
        url = reverse("index")
        assert url == "/"

    def test_url_login(self) -> None:
        """
        Test reverse match of login view.
        """
        url = reverse("login")
        assert url == "/login/"
