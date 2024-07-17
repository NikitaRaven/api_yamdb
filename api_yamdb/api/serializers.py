from rest_framework import serializers

from users.models import CustomUser
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
