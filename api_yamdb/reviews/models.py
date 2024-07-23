from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import reviews.constants as constants
from .validators import title_year_validator

User = get_user_model()


class NameSlugModel(models.Model):
    name = models.CharField(max_length=constants.CHAR_MAX_LEN,
                            verbose_name=constants.NAME_VERBOSE_NAME)
    slug = models.SlugField(unique=True,
                            max_length=constants.SLUG_MAX_LEN,
                            verbose_name=constants.SLUG_VERBOSE_NAME)

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug


class AuthorTextPubdateModel(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField(constants.VERBOSE_NAME_TEXT)
    pub_date = models.DateTimeField(
        constants.VERBOSE_NAME_PUB_DATE, auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class Genre(NameSlugModel):

    class Meta:
        verbose_name = constants.GENRE_VERBOSE_NAME
        verbose_name_plural = constants.GENRE_VERBOSE_NAME_PLURAL
        ordering = ('slug', )


class Category(NameSlugModel):

    class Meta:
        verbose_name = constants.CATEGORY_VERBOSE_NAME
        verbose_name_plural = constants.CATEGORY_VERBOSE_NAME_PLURAL
        ordering = ('slug', )


class Title(models.Model):
    name = models.CharField(max_length=constants.CHAR_MAX_LEN,
                            verbose_name=constants.NAME_VERBOSE_NAME)
    year = models.PositiveSmallIntegerField(
        validators=[title_year_validator],
        verbose_name=constants.TITLE_YEAR_VERBOSE_NAME
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=constants.TITLE_DESCRIPTIONS_VERBOSE_NAME
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name=constants.GENRE_VERBOSE_NAME_PLURAL
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True,
        verbose_name=constants.CATEGORY_VERBOSE_NAME
    )

    class Meta:
        ordering = ('id', 'name')
        verbose_name = constants.TITLE_VERBOSE_NAME
        verbose_name_plural = constants.TITLE_VERBOSE_NAME_PLURAL

    def __str__(self):
        return self.name


class Review(AuthorTextPubdateModel):
    score = models.SmallIntegerField(constants.VERBOSE_NAME_SCORE, validators=[
        MinValueValidator(constants.RATING_MIN, constants.RATING_MIN_VALIDATE),
        MaxValueValidator(constants.RATING_MAX, constants.RATING_MAX_VALIDATE)
    ])
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        related_name='reviews', blank=True, null=True
    )

    class Meta:
        verbose_name = constants.VERBOSE_NAME_REVIEW
        verbose_name_plural = constants.VERBOSE_NAME_REVIEW_PLURAL
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(AuthorTextPubdateModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = constants.VERBOSE_NAME_COMMENT
        verbose_name_plural = constants.VERBOSE_NAME_COMMENT_PLURAL
