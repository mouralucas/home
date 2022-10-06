from django.http import JsonResponse
from rest_framework.views import APIView

import BO.file.file
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


class Extract(APIView):
    def get(self, *args, **kwargs):
        path = self.request.GET.get('path')
        pdf_origin = self.request.GET.get('pdf_origin')

        response = BO.file.file.File().extract_table_pdf(path=path, pdf_origin=pdf_origin)

        return JsonResponse(response, safe=False)