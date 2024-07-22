from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import *
from .validators import title_year_validator

User = get_user_model()


class NameSlugModel(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LEN,
                            verbose_name=NAME_VERBOSE_NAME)
    slug = models.SlugField(unique=True,
                            max_length=SLUG_MAX_LEN,
                            verbose_name=SLUG_VERBOSE_NAME)

    class Meta:
        abstract = True
        ordering = ('slug', )
    
    def __str__(self):
        return self.slug

      
class BaseModel(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField(VERBOSE_NAME_TEXT)
    pub_date = models.DateTimeField(
        VERBOSE_NAME_PUB_DATE, auto_now_add=True, db_index=True)

    class Meta:
        abstract = True

        
class Genre(NameSlugModel):

    class Meta:
        verbose_name = GENRE_VERBOSE_NAME
        verbose_name_plural = GENRE_VERBOSE_NAME_PLURAL


class Category(NameSlugModel):

    class Meta:
        verbose_name = CATEGORY_VERBOSE_NAME
        verbose_name_plural = CATEGORY_VERBOSE_NAME_PLURAL


class Title(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LEN,
                            verbose_name=NAME_VERBOSE_NAME)
    year = models.PositiveSmallIntegerField(
        validators=[title_year_validator],
        verbose_name=TITLE_YEAR_VERBOSE_NAME
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=TITLE_DESCRIPTIONS_VERBOSE_NAME
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name=GENRE_VERBOSE_NAME_PLURAL
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True,
        verbose_name=CATEGORY_VERBOSE_NAME
    )

    class Meta:
        ordering = ('id', 'name')
        verbose_name = TITLE_VERBOSE_NAME
        verbose_name_plural = TITLE_VERBOSE_NAME_PLURAL

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """ Отдельная модель отношений между Title и Genre.
    Нужна для ипорта данных из csv"""

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
