from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import *

User = get_user_model()


class BaseModel(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField(VERBOSE_NAME_TEXT)
    pub_date = models.DateTimeField(
        VERBOSE_NAME_PUB_DATE, auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LEN)
    slug = models.SlugField(unique=True,
                            max_length=SLUG_MAX_LEN)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LEN)
    slug = models.SlugField(unique=True,
                            max_length=SLUG_MAX_LEN)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LEN)
    year = models.SmallIntegerField(validators=[
        MinValueValidator(YEAR_MIN)
    ])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = VERBOSE_NAME_TITLE
        verbose_name_plural = VERBOSE_NAME_TITLE_PLURAL
        ordering = ('id', 'name')


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(BaseModel):
    score = models.SmallIntegerField(VERBOSE_NAME_SCORE, validators=[
        MinValueValidator(RATING_MIN, RATING_MIN_VALIDATE),
        MaxValueValidator(RATING_MAX,RATING_MAX_VALIDATE)
    ])
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        related_name='reviews', blank=True, null=True
    )

    class Meta:
        verbose_name = VERBOSE_NAME_REVIEW
        verbose_name_plural = VERBOSE_NAME_REVIEW_PLURAL
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(BaseModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        verbose_name = VERBOSE_NAME_COMMENT
        verbose_name_plural = VERBOSE_NAME_COMMENT_PLURAL
