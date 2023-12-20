from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = _('Usuário não autenticado')

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CustomJWTAuthentication(JWTAuthentication):
    """
    :Name: CustomJWTAuthentication
    :Description: Class that overwrite JWTAuthentication
    :Created by: Lucas Penha de Moura - 09/12/2023
    :Edited by:

        This class overrides the default JWTAuthentication
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            # If there is no token user is AnonymousUser,
            # so it will not validate in classes with IsAuthenticated as permissions_classes
            # but will pass in open views
            return None
            # raise AuthenticationFailed(detail={'success': False, 'message': 'caraio manolo'}, code=status.HTTP_401_UNAUTHORIZED)

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )
