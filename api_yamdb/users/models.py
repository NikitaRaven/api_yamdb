from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    NAME_LENGTH, MAIL_LENGTH, CODE_LENGTH, ROLE_LENGTH, ROLE_CHOICES, USER
)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=NAME_LENGTH, unique=True)
    email = models.EmailField(max_length=MAIL_LENGTH, unique=True)
    first_name = models.CharField(max_length=NAME_LENGTH, blank=True)
    last_name = models.CharField(max_length=NAME_LENGTH, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=ROLE_LENGTH,
                            choices=ROLE_CHOICES,
                            default=USER)
    confirmation_code = models.CharField(max_length=CODE_LENGTH, blank=True)

    def __str__(self):
        return self.username
