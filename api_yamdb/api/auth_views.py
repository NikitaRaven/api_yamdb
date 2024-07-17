from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import CustomUser
from .serializers import CustomUserSerializer, AuthUserSerializer
from users.constants import CODE_LENGTH
from .error_constants import INVALID_EMAIL, INVALID_CODE, USER_NOT_FOUND


class SignUpView(generics.CreateAPIView):
    """Handle user registration and confirmation code sendig."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')

        existing_user = self.get_queryset().filter(
            username=username
        ).first()

        if existing_user:
            if existing_user.email != email:
                return Response(
                    {'error': INVALID_EMAIL},
                    status=status.HTTP_400_BAD_REQUEST
                )

            confirmation_code = get_random_string(length=CODE_LENGTH)
            existing_user.confirmation_code = confirmation_code
            existing_user.save()

            self.send_mail(confirmation_code, email)

            return Response({'username': existing_user.username,
                             'email': existing_user.email},
                            status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = get_random_string(length=CODE_LENGTH)
        serializer.save(confirmation_code=confirmation_code)

        self.send_mail(confirmation_code, email)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

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

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        user = self.get_queryset().filter(username=username).first()
        if not user:
            return Response({'error': USER_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)

        if user.confirmation_code != confirmation_code:
            return Response({'error': INVALID_CODE},
                            status=status.HTTP_400_BAD_REQUEST)

        access_token = AccessToken.for_user(user)
        return Response({'access': str(access_token)},
                        status=status.HTTP_200_OK)
