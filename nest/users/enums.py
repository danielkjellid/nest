from django.db.models import TextChoices


class AvatarColors(TextChoices):
    RED = "#F87171", "Red"
    YELLOW = "#FBBF24", "Yellow"
    GREEN = "#34D399", "Green"
    BLUE = "#60A5FA", "Blue"
    PURPLE = "#A78BFA", "Purple"
    PINK = "#F472B6", "Pink"
