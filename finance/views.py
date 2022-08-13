from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

import util.datetime


class Home(APIView):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        context = {
            'periodos': util.datetime.DateTime().list_period(),
        }

        return render(self.request, 'finance/landingpage.html', context=context)


class Configuracoes(APIView):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        context = {}

        return render(self.request, 'finance/settings.html')