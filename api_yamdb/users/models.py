from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import (
    NAME_LENGTH, MAIL_LENGTH, CODE_LENGTH, ROLE_LENGTH, ROLE_CHOICES, USER,
    MODERATOR, ADMIN, CUSTOM_USER_VERBOSE, CUSTOM_USER_VERBOSE_PLURAL,
    VERBOSE_NAME_USERNAME, VERBOSE_NAME_EMAIL, VERBOSE_NAME_FIRST_NAME,
    VERBOSE_NAME_LAST_NAME, VERBOSE_NAME_BIO, VERBOSE_NAME_ROLE,
    VERBOSE_NAME_CONFIRMATION_CODE
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=NAME_LENGTH,
        unique=True,
        verbose_name=VERBOSE_NAME_USERNAME
    )
    email = models.EmailField(
        max_length=MAIL_LENGTH,
        unique=True,
        verbose_name=VERBOSE_NAME_EMAIL
    )
    first_name = models.CharField(
        max_length=NAME_LENGTH,
        blank=True,
        verbose_name=VERBOSE_NAME_FIRST_NAME
    )
    last_name = models.CharField(
        max_length=NAME_LENGTH,
        blank=True,
        verbose_name=VERBOSE_NAME_LAST_NAME
    )
    bio = models.TextField(blank=True, verbose_name=VERBOSE_NAME_BIO)
    role = models.CharField(
        max_length=ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name=VERBOSE_NAME_ROLE
    )
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        blank=True,
        verbose_name=VERBOSE_NAME_CONFIRMATION_CODE
    )

    class Meta:
        verbose_name = CUSTOM_USER_VERBOSE
        verbose_name_plural = CUSTOM_USER_VERBOSE_PLURAL

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
