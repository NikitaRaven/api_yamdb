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
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id', 'name')


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    text = models.TextField()
    score = models.SmallIntegerField(validators=[
        MinValueValidator(reviews.constants.RATING_MIN,
                          "Оценка не ожет быть меньше 0"),
        MaxValueValidator(reviews.constants.RATING_MAX,
                          "Оценка не ожет быть больше 10")
    ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        related_name='reviews', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
