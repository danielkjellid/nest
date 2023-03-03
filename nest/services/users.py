from typing import Any
from nest.records import UserRecord
from nest.exceptions import ApplicationError
from nest.models import User
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError as DjangoValidationError


class UserService:
    def __init__(self) -> None:
        ...

    @classmethod
    def create(
        cls,
        email: str,
        password: str | None = None,
        password2: str | None = None,
        is_active: bool = True,
        **additional_fields: Any,
    ) -> UserRecord:
        """
        Creates a new user instance.
        """

        validated_email, validated_password = cls._validate_email_and_password(
            email=email, password=password, password2=password2
        )

        new_user = User(email=validated_email, is_active=is_active, **additional_fields)
        new_user.set_password(raw_password=validated_password)
        new_user.save()

        return UserRecord.from_user(new_user)

    @staticmethod
    def _validate_email_and_password(
        email: str, password: str | None, password2: str | None
    ) -> tuple[str, str]:
        """
        Validate email and password for create operation
        """

        if not email:
            raise ApplicationError(
                message="Error when creating user, email cannot be none.",
                extra={"email": "This field cannot be empty."},
            )

        if not password:
            raise ApplicationError(
                message="Error when creating user, password cannot be none.",
                extra={"password": "This field cannot be empty."},
            )

        if password and password2:
            if password != password2:
                raise ApplicationError(
                    message="The two password fields didn't match.",
                    extra={
                        "password": "The two password fields didn't match.",
                        "password2": "The two password fields didn't match.",
                    },
                )

        existing_user = User.objects.filter(email__iexact=email).exists()

        if existing_user:
            raise ApplicationError(
                message="Email is already registered.",
                extra={"email": "Email is already registered."},
            )

        try:
            validate_email(email)
            validate_password(password=password)
        except DjangoValidationError as exc:
            raise ApplicationError(message=str(exc)) from exc

        return email, password
