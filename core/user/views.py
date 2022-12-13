from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import BO.user.account
import BO.user.login


class Login(TokenObtainPairView):
    """
    :Nome da classe/função: Login
    :Descrição: View de login de usuário Venda+
    :Criação: Lucas Penha de Moura - 01/02/2021
    :Edições:
    """
    serializer_class = BO.user.login.Login


class Account(APIView):
    def get(self, *args, **kwargs):
        return render(self.request, '')

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        raw_password = self.request.POST.get('raw_password')

        response = BO.user.account.Account(username=username, raw_password=raw_password).create()

        return JsonResponse(response, safe=False)
