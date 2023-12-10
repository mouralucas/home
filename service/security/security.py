from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = _('Usuário não autenticado')

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)




