from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Review(models.Model):
    text = models.TextField()
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(reviews.constants.RATING_MIN),
        MaxValueValidator(reviews.constants.RATING_MAX)
    ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        related_name='reviews', blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
