from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .auth_views import SignUpView, TokenObtainView
from .user_views import CustomUserViewSet


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/',
         TokenObtainView.as_view(),
         name='token_obtain'),
    path('v1/', include(router.urls)),
]
