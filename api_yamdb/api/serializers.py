from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from users.models import CustomUser
from reviews.models import Title, Category, Genre, Review, Comment
from users.constants import NAME_LENGTH, MAIL_LENGTH
from .error_constants import (
    INVALID_USERNAME, ME_NOT_ALLOWED, INVALID_SLUG_MAX_LEN, INVALID_YEAR,
    INVALID_REVIEW, INVALID_EMAIL, USER_NOT_FOUND, INVALID_CODE,
    EMAIL_MISMATCH
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

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=NAME_LENGTH,
        error_messages={
            'invalid': INVALID_USERNAME
        }
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(ME_NOT_ALLOWED)
        return value

    def validate_email(self, value):
        username = self.initial_data.get('username')
        existing_user = CustomUser.objects.filter(username=username).first()
        if existing_user and existing_user.email != value:
            raise serializers.ValidationError(INVALID_EMAIL)

        existing_mail = CustomUser.objects.filter(email=value).first()
        if existing_mail and existing_mail.username != username:
            raise serializers.ValidationError(EMAIL_MISMATCH)

        return value


class CustomUserSerializer(BaseUserSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(BaseUserSerializer):

    email = serializers.EmailField(max_length=MAIL_LENGTH)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')

        user = CustomUser.objects.filter(
            username=username,
            email=email
        ).first()

        if not user:
            return CustomUser.objects.create(**validated_data)

        user.confirmation_code = validated_data.get('confirmation_code')
        user.save()
        return user


class AuthUserSerializer(BaseUserSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')

    def validate(self, value):
        user = CustomUser.objects.filter(
            username=value.get('username')
        ).first()

        if not user:
            raise NotFound(USER_NOT_FOUND)

        if user.confirmation_code != value.get('confirmation_code'):
            raise serializers.ValidationError(INVALID_CODE)

        return value


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
        review = Review.objects.filter(
            title=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user
        )
        if request.method == 'POST' and review.exists():
            raise serializers.ValidationError(INVALID_REVIEW)
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
