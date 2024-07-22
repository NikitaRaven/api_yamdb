from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import (
    NAME_LENGTH, MAIL_LENGTH, CODE_LENGTH, ROLE_LENGTH, ROLE_CHOICES, USER,
    MODERATOR, ADMIN, USER_VERBOSE, USER_VERBOSE_PLURAL, USERNAME, EMAIL,
    FIRST_NAME, LAST_NAME, BIO, ROLE, CONFIRMATION_CODE
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=NAME_LENGTH,
        unique=True,
        verbose_name=USERNAME
    )
    email = models.EmailField(
        max_length=MAIL_LENGTH,
        unique=True,
        verbose_name=EMAIL
    )
    first_name = models.CharField(
        max_length=NAME_LENGTH,
        blank=True,
        verbose_name=FIRST_NAME
    )
    last_name = models.CharField(
        max_length=NAME_LENGTH,
        blank=True,
        verbose_name=LAST_NAME
    )
    bio = models.TextField(blank=True, verbose_name=BIO)
    role = models.CharField(
        max_length=ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name=ROLE
    )
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        blank=True,
        verbose_name=CONFIRMATION_CODE
    )

    class Meta:
        verbose_name = USER_VERBOSE
        verbose_name_plural = USER_VERBOSE_PLURAL

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN
