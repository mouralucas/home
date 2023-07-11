from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import BO.core.core
import util.datetime


class Country(APIView):
    def get(self, *args, **kwargs):
        response = BO.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)


class Module(APIView):
    def get(self, *args, **kwargs):
        selected_id = self.request.query_params.get('selected_id')

        response = BO.core.core.Misc().get_module(id_selected=selected_id)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        pass


class Category(APIView):
    def get(self, *args, **kwargs):
        show_mode = self.request.query_params.get('show_mode')
        module = self.request.query_params.get('module')

        response = BO.core.core.Misc().get_category(show_mode=show_mode, module_id=module)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        pass


class Period(APIView):
    def get(self, *args, **kwargs):
        periods = util.datetime.DateTime().list_period()

        return JsonResponse(periods, safe=False)


class Status(APIView):
    def get(self, *args, **kwargs):
        status_type = self.request.GET.get('status_type')

        response = BO.core.core.Misc().get_status(status_type=status_type)

        return JsonResponse(response, safe=False)


class State(APIView):
    def get(self, *args, **kwargs):
        response = BO.core.core.Misc().get_states()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        """
        Teste de ação post do ReactJS
        """
        name = self.request.POST.get('txtNome')

        response = {
            'status': True,
            'mensagem': 'O post deu boa, truta!, o nome é {}'.format(name)
        }

        return Response(response, status=200)


class Version(APIView):
    def get(self, *args, **kwargs):

        response = BO.core.core.Misc().get_version()

        return Response(response, status=200)