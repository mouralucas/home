from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView

import BO.core.core


class Country(View):
    def get(self, *args, **kwargs):
        response = BO.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)


class Module(View):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id')

        response = BO.core.core.Misc().get_module(id_selected=selected_id)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        pass


class Category(View):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id')
        show_mode = self.request.GET.get('show_mode')
        module = self.request.GET.get('module')

        # response = BO.finance.finance.Finance().get_category(selected_id=selected_id)
        response = BO.core.core.Misc().get_category(show_mode=show_mode, module_id=module, selected_id=selected_id)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        pass


class State(APIView):
    def get(self, *args, **kwargs):
        response = BO.core.core.Misc().get_states()

        return JsonResponse(response, safe=False)
