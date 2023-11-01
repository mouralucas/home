from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import service.user.account
import service.user.login

from core.user.serializers import AccountPostSerializer


class Login(TokenObtainPairView):
    """
    :Name: Login
    :Description: View for user login
    :Created by: Lucas Penha de Moura - 01/02/2021
    :Edited by:

    Explicit params:
    username: the username of the user
    password: the password of the user

        Implements TokenObtainPairView from simple jwt
    """
    serializer_class = service.user.login.Login


class Account(APIView):
    def get(self, *args, **kwargs):
        return render(self.request, '')

    def post(self, *args, **kwargs):
        data = AccountPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        username = data.validated_data.get('username')
        raw_password = data.validated_data.get('rawPassword')

        response = service.user.account.Account(username=username, raw_password=raw_password).create()

        return JsonResponse(response, safe=False)
