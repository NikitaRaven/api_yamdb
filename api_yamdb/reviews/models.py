from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

import reviews.constants

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=reviews.constants.CHAR_MAX_LEN)
    slug = models.SlugField(unique=True,
                            max_length=reviews.constants.SLUG_MAX_LEN)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=reviews.constants.CHAR_MAX_LEN)
    slug = models.SlugField(unique=True,
                            max_length=reviews.constants.SLUG_MAX_LEN)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=reviews.constants.CHAR_MAX_LEN)
    year = models.SmallIntegerField(validators=[
        MinValueValidator(reviews.constants.YEAR_MIN)
    ])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True,
    )

    def __str__(self):
        return self.name
