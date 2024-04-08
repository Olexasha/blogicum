from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about_me = models.TextField(
        verbose_name="Биография", blank=True, default=""
    )

    def __str__(self):
        return self.username
