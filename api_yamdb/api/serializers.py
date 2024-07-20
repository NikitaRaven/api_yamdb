from datetime import datetime

from rest_framework import serializers

from users.models import CustomUser
from reviews.models import Title, Category, Genre, Review, Comment
from users.constants import NAME_LENGTH
from .error_constants import (
    INVALID_USERNAME, ME_NOT_ALLOWED, INVALID_SLUG_MAX_LEN, INVALID_YEAR
)


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


class CategorySerializer(serializers.ModelSerializer):

    def validate_slug(self, value):
        if len(value) >= 50:
            raise serializers.ValidationError(INVALID_SLUG_MAX_LEN)
        return value

    class Meta:
        model = Category
        exclude = ('id', )
        ordering = ('slug', )


class GenreSerializer(serializers.ModelSerializer):

    def validate_slug(self, value):
        if len(value) >= 50:
            raise serializers.ValidationError(INVALID_SLUG_MAX_LEN)
        return value

    class Meta:
        model = Genre
        exclude = ('id', )
        ordering = ('slug', )


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
    rating = serializers.SerializerMethodField()

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(INVALID_YEAR)
        return value

    def get_rating(self, obj):
         reviews = Review.objects.filter(title=obj)
         if bool(reviews):
            return round(sum(review.score for review in reviews)
                         / len(reviews), 1)
         return None

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

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
