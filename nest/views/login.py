from .base import ReactView
from django.contrib.auth.views import LoginView as DjangoLoginView


class LoginView(ReactView, DjangoLoginView):
    template_name = "login.html"
    index_path = "frontend/apps/login/index.tsx"
