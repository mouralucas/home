from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = 'Usuário não authenticado'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)