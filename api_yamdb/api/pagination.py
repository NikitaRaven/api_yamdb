from rest_framework.pagination import LimitOffsetPagination

from .constants import DEFAULT_PAGE_SIZE


class UserPaginatior(LimitOffsetPagination):
    """Individual paginator for CustomUser model."""

    default_limit = DEFAULT_PAGE_SIZE
