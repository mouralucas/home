from rest_framework.response import Response
from rest_framework.views import APIView

import service.integration.bcb


class Historical(APIView):
    def get(self, *args, **kwargs):
        a = service.integration.bcb.BancoCentralAPI().historical_data_cdi()
        b = service.integration.bcb.BancoCentralAPI().historical_data_selic()
        c = service.integration.bcb.BancoCentralAPI().historical_data_ipca()

        return Response({}, status=200)
