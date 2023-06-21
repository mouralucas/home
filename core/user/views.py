from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import BO.user.account
import BO.user.login


class Login(TokenObtainPairView):
    """
    :Name: Login
    :Description: View for user login
    :Created by: Lucas Penha de Moura - 01/02/2021
    :Edited by:

    Explicit params:
    None

    Implicit params (passed in the class instance or set by other functions):
    None

        Implements TokenObtainPairView from simple jwt
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
