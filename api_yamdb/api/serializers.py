from datetime import datetime

from rest_framework import serializers

from users.models import CustomUser
from reviews.models import Title, Category, Genre, Review, Comment
from users.constants import NAME_LENGTH
from .error_constants import INVALID_USERNAME, ME_NOT_ALLOWED


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
    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                "You can't add works that haven't been released yet"
            )
        return value

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
