from django.http import JsonResponse
from rest_framework.views import APIView

import BO.file.file
import file.models


class Upload(APIView):
    def get(self, *args, **kwargs):
        file = file.models.File.objects.first()

        response = {
            'url': file.file.url
        }

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        file = self.request.FILES.get('file')

        file_m = file.models.File()
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