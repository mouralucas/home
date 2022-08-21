from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import BO.user.account
from datetime import datetime, timedelta


class LoginDjango(BO.user.account.Account):
    def __init__(self, username=None, raw_password=None, request=None):
        super(LoginDjango, self).__init__(username=username, raw_password=raw_password)
        self.request = request

    def authenticate(self):
        """
        :Name: authenticate
        :Created by: Lucas Penha de Moura - 09/06/2022
        :Edited by:

        Check if all data is correct for the user and log the user into the system.
        Create the user session with all information needed to navigate
        """

        # Check if all data is available
        if not self.username or not self.raw_password:
            return {'status': False, 'description': 'All fields are needed', 'redirect': ''}

        # Authenticate the user
        self.user = authenticate(username=self.username, password=self.raw_password)
        if not self.user:
            return {'status': False, 'description': 'User or passwor not found!', 'redirect': ''}

        # Log the user
        login(self.request, self.user)

        # Create the session
        pass

        response = {
            'status': True,
            'redirect': ''
        }

        return response

    def logout(self):
        """
        :Name: logout
        :Created by: Lucas Penha de Moura - 09/06/2022
        :Edited by:

        Log the user out of the system
        """
        logout(self.request)

        response = {
            'status': True,
            'redirect': ''
        }

        return response

    authenticate.__doc__ = 'Used the authenticate a user into the system'


class LoginSerializer(TokenObtainPairSerializer):
    """
    :Nome da classe/função: LoginApiSerializer
    :Descrição: Classe de serializaçaõ do login da API
    :Criação: Lucas Penha de Moura - 04/11/2020
    :Edições:
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        """
        :Name: validate
        :Created by: Lucas Penha de Moura - 04/11/2020
        :Edited by:

            Handles the username and password from the user loggin in
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
            data = {
                'expire': datetime.now() + timedelta(days=1),
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }

            return data

        else:
            raise serializers.ValidationError({'error': _('Usuário e senhas são campos obrigatórios')})


class Login(LoginSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_serializer_class(self):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = user.username
        # token['matricula'] = user

        # usr_info = BO.autenticacao.sessao.SessaoFuncionario().criar_sessao_funcionario(user=user)

        # token['view_inicial'] = usr_info['view_inicial']
        # token['is_loja'] = True if usr_info['perfil_principal'] == 'loja' else False

        return token
