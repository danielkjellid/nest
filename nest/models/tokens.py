from django.db import models


class OutstandingToken(models.Model):
    user = models.ForeignKey(
        "nest.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tokens",
    )

    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()

    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        app_label = "nest"
        verbose_name = "Outstanding token"
        verbose_name_plural = "Outstanding tokens"

    def __str__(self) -> str:
        return f"Token for {self.user} ({self.jti})"


class BlacklistedToken(models.Model):
    token = models.OneToOneField(
        "nest.OutstandingToken",
        on_delete=models.CASCADE,
        related_name="blacklisted_token",
    )
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "nest"
        verbose_name = "Blacklisted token"
        verbose_name_plural = "Blacklisted tokens"

    def __str__(self) -> str:
        return f"Blacklisted token for {self.token.user}"
