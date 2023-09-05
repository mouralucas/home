from rest_framework.response import Response
from rest_framework.views import APIView
import service.finance.finance

class Currency(APIView):
    def get(self, *args, **kwargs):
        response = service.finance.finance.Finance().get_currency()

        return Response(response, status=200)