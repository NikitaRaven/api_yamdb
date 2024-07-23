from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import CustomUser
from users.constants import CODE_LENGTH
from .serializers import SignUpSerializer, AuthUserSerializer


class SignUpView(generics.CreateAPIView):
    """Handle user registration and confirmation code sending."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        confirmation_code = get_random_string(length=CODE_LENGTH)
        serializer.save(confirmation_code=confirmation_code)
        self.send_mail(confirmation_code, serializer.validated_data['email'])

    def send_mail(self, confirmation_code, email):
        subject = 'Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = (email,)
        send_mail(subject, message, from_email, recipient_list)


class TokenObtainView(generics.CreateAPIView):
    """Grant access token in exchange for confirmation code."""

    queryset = CustomUser.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        user = self.get_queryset().filter(username=username).first()

        access_token = AccessToken.for_user(user)
        return Response({'access': str(access_token)},
                        status=status.HTTP_200_OK)
