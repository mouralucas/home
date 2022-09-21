from django.http import JsonResponse
from rest_framework.views import APIView

import file_manager.models


class Upload(APIView):
    def get(self, *args, **kwargs):
        file = file_manager.models.File.objects.first()

        response = {
            'url': file.file.url
        }

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        file = self.request.FILES.get('file')

        file_m = file_manager.models.File()
        file_m.file = file
        file_m.save()
        response = {}

        return JsonResponse(response, safe=False)

