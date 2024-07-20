from rest_framework import permissions

from users.constants import ADMIN, MODERATOR


class AdminOrSuperOrSelf(permissions.BasePermission):
    """
    Admin and superuser can alter user profiles.
    Users can access and alter only their profiles.
    """

    def has_permission(self, request, view):
        return (request.user.role == ADMIN
                or request.user.is_staff
                or view.kwargs.get('username') == 'me')


class CategoryGenreTitlePermission(permissions.BasePermission):
    """
    Admin and superuser have 'POST', 'DELETE' and 'PATCH' permissions.
    Users have read only access.
    """

    def has_permission(self, request, view):
        if request.method in ('POST', 'DELETE', 'PATCH'):
            user = request.user
            return (user.is_authenticated
                    and (user.role == ADMIN or user.is_staff))

        return True


class ReviewCommentsPermission(permissions.BasePermission):
    """
    Staff have 'POST', 'DELETE' and 'PATCH' permissions.
    Users have 'GET', 'POST' and (if author) 'DELETE' permissions.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PATCH'):
            user = request.user
            return (user.is_authenticated
                    and (obj.author == user
                         or user.role in (ADMIN, MODERATOR)
                         or user.is_staff))

        return True
