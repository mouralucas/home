from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView


class PagSeguroImportStatement(APIView):
    @extend_schema()
    def post(self, *args, **kwargs):
        pass