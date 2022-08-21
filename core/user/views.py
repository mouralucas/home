from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework_simplejwt.views import TokenObtainPairView

import BO.user.login
import BO.user.account


class Login(TokenObtainPairView):
    """
    :Nome da classe/função: Login
    :Descrição: View de login de usuário Venda+
    :Criação: Lucas Penha de Moura - 01/02/2021
    :Edições:
    """
    print('')
    serializer_class = BO.user.login.Login


class LoginDjango(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'user/login.html')

    def post(self, *args, **kwargs):
        """
        :Name: Login - post
        :Created by: Lucas Penha de Moura - 09/06/2022
        :Edited by:

        Handles the input data and send to BO the proccess the login
        """
        username = self.request.POST.get('username')
        raw_password = self.request.POST.get('raw_password')

        response = BO.user.login.LoginDjango(username=username, raw_password=raw_password, request=self.request).authenticate()

        # return render(self.request, response['redirect'], context=response)
        return HttpResponseRedirect(reverse('finance:home'))


class Account(View):
    def get(self, *args, **kwargs):
        return render(self.request, '')

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        raw_password = self.request.POST.get('raw_password')

        response = BO.user.account.Account(username=username, raw_password=raw_password).create()

        return JsonResponse(response, safe=False)
