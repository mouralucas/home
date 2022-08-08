from django.http import JsonResponse
from django.views import View
import BO.core.core


class Country(View):
    def get(self, *args, **kwargs):
        response = BO.core.core.Misc().get_country()

        return JsonResponse(response, safe=False)
