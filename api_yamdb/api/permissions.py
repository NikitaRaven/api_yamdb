from rest_framework import permissions

from users.constants import ADMIN, MODERATOR


class AdminOrSuperOrSelf(permissions.BasePermission):
    """
    Admin and superuser can alter user profiles.
    Users can access and alter only their profiles.
    """

    def has_permission(self, request, view):
        if request.user.role == ADMIN or request.user.is_staff:
            return True

        if view.kwargs.get('username') == 'me':
            return True

        return False


class CategoryGenrePermission(permissions.BasePermission):
    """
    Admin and superuser have POST and DELETE permissions.
    Users have read only access.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method in ('POST', 'DELETE'):
            user = request.user
            return user.role == ADMIN or user.is_staff

        return False


class TitlePermission(permissions.BasePermission):
    """
    Admin and superuser have 'POST', 'DELETE' and 'PATCH' permissions.
    Users have read only access.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method in ('POST', 'DELETE', 'PATCH'):
            user = request.user
            return user.role == ADMIN or user.is_staff

        return False


class ReviewCommentsPermission(permissions.BasePermission):
    """
    Staff have 'POST', 'DELETE' and 'PATCH' permissions.
    Users have 'GET', 'POST' and (if author) 'DELETE' permissions.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        if request.method == 'POST':
            return request.user.is_authenticated

        if request.method in ('DELETE', 'PATCH'):
            user = request.user
            return (obj.author == user
                    or user.role in (ADMIN, MODERATOR)
                    or user.is_staff)

        return False
