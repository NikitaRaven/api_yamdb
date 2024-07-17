from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import CustomUserSerializer
from .pagination import UserPaginatior
from .permissions import AdminOrSuperOrSelf


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, AdminOrSuperOrSelf)
    pagination_class = UserPaginatior
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
            return Response({'error': f'{username} already exist'},
                            status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        if not partial:
            return Response({'error': 'put is not allowed'},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        elif kwargs.get('username') == 'me':
            kwargs['username'] = self.request.user.username
            if request.data.get('role'):
                return Response({'error': 'No role change at this endpoint'},
                                status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response({'error': 'only stuff can delete'},
                            status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
