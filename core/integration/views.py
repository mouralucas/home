from rest_framework.response import Response
from rest_framework.views import APIView

import service.integration.vat_rate
from service.security.security import IsAuthenticated


# Create your views here.
class CurrencyRate(APIView):
    # authentication_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date = self.request.query_params.get('date')

        response = service.integration.vat_rate.Vat().get_currency_rate(date=date)

        return Response(response)
