from __future__ import annotations

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token, BlacklistMixin
from rest_framework_simplejwt.utils import format_lazy, datetime_from_epoch

import service.core.cache


class CustomToken(Token):
    def __init__(self, token=None, verify=True):
        self.redis_instance = service.core.cache.LoginTokens()
        self.redis = self.redis_instance.get_connection()
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

        try:
            claim_id = self.payload['jti']
        except KeyError:
            raise TokenError(format_lazy(_("Token has no '{}' claim"), "jti"))

        # if not present in Redis it raises an exception
        user_token = self.redis.get(claim_id)
        if not user_token:
            raise TokenError(format_lazy(_("Token was revoked"), claim))

        claim_time = datetime_from_epoch(claim_value)
        leeway = self.get_token_backend().get_leeway()
        if claim_time <= current_time - leeway:
            raise TokenError(format_lazy(_("Token '{}' claim has expired"), claim))


class CustomAccessToken(CustomToken):
    """
    :Name: CustomAccessToken
    :Description: Class that overwrite AccessToken
    :Created by: Lucas Penha de Moura - 09/12/2023
    :Edited by:

        This class overrides the default AccessToken class to allow check the token using Redis cache
    """
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME


class CustomRefreshToken(BlacklistMixin, CustomToken):
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        api_settings.JTI_CLAIM,
        "jti",
    )
    access_token_class = CustomAccessToken

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = self.access_token_class()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


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


class Login(TokenObtainSerializer):
    token_class = CustomRefreshToken

    def __init__(self, *args, **kwargs):
        self.redis_instance = service.core.cache.LoginTokens()
        self.redis = self.redis_instance.get_connection()
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        """
        :Name: validate
        :Created by: Lucas Penha de Moura - 04/11/2020
        :Edited by:

            Handles the username and password from the user log in
        """

        try:
            request = self.context["request"]
        except KeyError:
            raise serializers.ValidationError({'error': _('Houve um erro na autenticação')})

        if request:
            request_data = request.data
        else:
            raise serializers.ValidationError({'error': _('Houve um erro na autenticação')})

        if "username" in request_data and "password" in request_data:
            user = authenticate(username=request_data['username'], password=request_data['password'])

            if not user:
                raise serializers.ValidationError({'error': _('Usuário ou senha inválidos')})

            refresh = self.get_token(user=user)
            access_token = refresh.access_token

            # Add tokens to redis (yet to create the value field, maybe will contain permissions data in access token)
            self.redis.set(access_token.payload['jti'], 'value', access_token.payload['exp'])
            self.redis.set(refresh.payload['jti'], 'value_refresh', refresh.payload['exp'])

            # return refresh
            return {'access': str(access_token), 'refresh': str(refresh)}
        else:
            raise serializers.ValidationError({'error': _('Usuário e senhas são campos obrigatórios')})


class Refresh(TokenRefreshSerializer):
    token_class = CustomRefreshToken

    def __init__(self, **kwargs):
        self.redis_instance = service.core.cache.LoginTokens()
        self.redis = self.redis_instance.get_connection()
        super().__init__(**kwargs)

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        access_token = refresh.access_token
        data = {"access": str(access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            try:
                # Remove Redis reference
                claim_id = refresh.payload['jti']
                self.redis.delete(claim_id)
            except KeyError:
                raise TokenError(format_lazy(_("Token has no '{}' claim"), "jti"))

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            self.redis.set(access_token.payload['jti'], 'value', access_token.payload['exp'])
            self.redis.set(refresh.payload['jti'], 'value_refresh', refresh.payload['exp'])

            data["refresh"] = str(refresh)

        return data
