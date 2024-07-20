from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import AdminOrSuperOrSelf
from .error_constants import (
    USER_EXISTS, USER_NO_PUT, NO_ROLE_CHANGE, ONLY_STAFF_DELETE
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, AdminOrSuperOrSelf)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            return self.get_queryset().filter(
                username=self.request.user.username
            ).first()
        return super().get_object()

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        existing_user = self.get_queryset().filter(
            username=username
        ).first()

        if existing_user:
            return Response({'error': USER_EXISTS},
                            status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        if not partial:
            return Response({'error': USER_NO_PUT},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        elif kwargs.get('username') == 'me':
            kwargs['username'] = self.request.user.username
            if request.data.get('role'):
                return Response({'error': NO_ROLE_CHANGE},
                                status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response({'error': ONLY_STAFF_DELETE},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
