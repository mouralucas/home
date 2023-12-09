from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = _('Usuário não autenticado')

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

