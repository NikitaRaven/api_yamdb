from rest_framework import mixins, viewsets
from rest_framework import filters

from .permissions import (CategoryGenreTitlePermission)


class CreateListDestroySearchSlugMixin(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (CategoryGenreTitlePermission,)
