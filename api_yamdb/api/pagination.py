from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class UserPaginatior(LimitOffsetPagination):
    """Individual paginator for CustomUser model."""

    default_limit = settings.REST_FRAMEWORK.get('PAGE_SIZE')
