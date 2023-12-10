from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.utils import format_lazy, datetime_from_epoch


class CustomAccessToken(AccessToken):
    """
    :Name: CustomAccessToken
    :Description: Class that overwrite AccessToken
    :Created by: Lucas Penha de Moura - 09/12/2023
    :Edited by:

        This class overrides the default AccessToken class to allow check the token using Redis cache
    """
    def __init__(self, token=None, verify=True):
        super().__init__(token=token, verify=verify)

    def check_exp(self, claim="exp", current_time=None):
        """
        Checks whether a timestamp value in the given claim has passed (since
        the given datetime value in `current_time`).  Raises a TokenError with
        a user-facing error message if so.

        The overwrite check if the token is valid using Redis.
        If not present in Redis, it could be revoked or expired, so raise a TokenError
        """
        if current_time is None:
            current_time = self.current_time

        try:
            claim_value = self.payload[claim]
        except KeyError:
            raise TokenError(format_lazy(_("Token has no '{}' claim"), claim))

        claim_time = datetime_from_epoch(claim_value)
        leeway = self.get_token_backend().get_leeway()
        if claim_time <= current_time - leeway:
            raise TokenError(format_lazy(_("Token '{}' claim has expired"), claim))


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
            return None

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
