from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings

import service.core.cache
from base.serializers import CustomSerializer
from service.security.login import CustomRefreshToken


class LoginSerializer(TokenObtainSerializer):
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


class RefreshSerializer(TokenRefreshSerializer):
    token_class = CustomRefreshToken

    def __init__(self, **kwargs):
        self.redis_instance = service.core.cache.LoginTokens()
        self.redis = self.redis_instance.get_connection()
        super().__init__(**kwargs)

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data


class AccountGetSerializer(CustomSerializer):
    caralhosVoadores = serializers.CharField(required=False)


class AccountPostSerializer(CustomSerializer):
    username = serializers.CharField(required=True)
    rawPassword = serializers.CharField(required=True)
