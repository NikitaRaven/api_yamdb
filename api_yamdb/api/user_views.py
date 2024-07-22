from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import AdminOrSuperOrSelf
from .error_constants import USER_NO_PUT, NO_ROLE_CHANGE, ONLY_STAFF_DELETE


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

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial'):
            return Response({'error': USER_NO_PUT},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        if kwargs.get('username') == 'me' and request.data.get('role'):
            return Response({'error': NO_ROLE_CHANGE},
                            status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response({'error': ONLY_STAFF_DELETE},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
