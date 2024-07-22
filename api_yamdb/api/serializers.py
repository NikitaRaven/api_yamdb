from datetime import datetime

from rest_framework import serializers

from users.models import CustomUser
from reviews.models import Title, Category, Genre, Review, Comment
from users.constants import NAME_LENGTH
from .error_constants import (
    INVALID_USERNAME, ME_NOT_ALLOWED, INVALID_SLUG_MAX_LEN, INVALID_YEAR
)
from .constants import ORDER_BY_SLUG


class ValidateSlugSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = (ORDER_BY_SLUG, )

    def validate_slug(self, value):
        if len(value) >= 50:
            raise serializers.ValidationError(INVALID_SLUG_MAX_LEN)
        return value


class CategoryGenreSlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, value):
        obj = self.queryset.get(slug=value)
        return {'name': obj.name,
                'slug': obj.slug}


class BaseUserSerializer(serializers.ModelSerializer):

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=NAME_LENGTH,
        error_messages={
            'invalid': INVALID_USERNAME
        }
    )

    class Meta:
        model = CustomUser
        fields = ('username',)


class CustomUserSerializer(BaseUserSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(ME_NOT_ALLOWED)
        return value

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name', 'last_name', 'bio', 'role'
        )


class AuthUserSerializer(BaseUserSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class CategorySerializer(ValidateSlugSerializer):

    class Meta:
        model = Category
        exclude = ('id',)

class GenreSerializer(ValidateSlugSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryGenreSlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = CategoryGenreSlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(INVALID_YEAR)
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            review = Review.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user
            )
            if review.exists():
                raise serializers.ValidationError(
                    'Ваш отзыв на это произведение уже опубликован'
                )
        return data

    class Meta:

        model = Review
        fields = ('id', 'text', 'author', 'pub_date', 'title', 'score')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментов."""

    review = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:

        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
