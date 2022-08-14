from django.http import JsonResponse
from django.views import View

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
