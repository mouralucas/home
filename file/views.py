from django.http import JsonResponse
from rest_framework.views import APIView

import service.file.file
import file.models


class Upload(APIView):
    def get(self, *args, **kwargs):
        files = file.models.File.objects.first()

        response = {
            'url': files.file.url
        }

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        files = self.request.FILES.get('files[]')

        file_m = file.models.File()
        file_m.file = files
        file_m.save()

        new_file = file.models.File.objects.filter(pk=file_m.pk).first()
        response = {
            'path': new_file.file.url
        }

        return JsonResponse(response, safe=False)


class Extract(APIView):
    def get(self, *args, **kwargs):
        path = self.request.GET.get('path')
        pdf_origin = self.request.GET.get('pdf_origin')

        response = service.file.file.File().extract_table_pdf(path=path, pdf_origin=pdf_origin)

        return JsonResponse(response, safe=False)