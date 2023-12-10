import uuid
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from service.security.security import CustomAccessToken


class Login(TokenObtainPairSerializer):
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
            # data = {
            #     'expire': datetime.now() + timedelta(days=1),
            #     'access': str(refresh.access_token),
            #     'refresh': str(refresh),
            # }

            return refresh

        else:
            raise serializers.ValidationError({'error': _('Usuário e senhas são campos obrigatórios')})

    @classmethod
    def get_token(cls, user):

        now = timezone.now()
        access_token_expire = now + timezone.timedelta(minutes=15)
        refresh_token_expire = now + timezone.timedelta(days=30)
        issue_date = now

        access_token_id = str(uuid.uuid4())
        refresh_token_id = str(uuid.uuid4())

        # Generate access token
        access_token = CustomAccessToken()
        access_token_payload = {
            'user_id': str(user.id),
            'token_type': 'access',
            'exp': access_token_expire,
            'iat': issue_date,
            'jti': access_token_id
        }
        access_token.payload = access_token_payload

        # Generate refresh token
        refresh_token = RefreshToken()
        refresh_token_payload = {
            'user_id': str(user.id),
            'token_type': 'refresh',
            'exp': refresh_token_expire,
            'iat': issue_date,
            'jti': refresh_token_id
        }
        refresh_token.payload = refresh_token_payload

        return {'access': str(access_token), 'refresh': str(refresh_token)}
