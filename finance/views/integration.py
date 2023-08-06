from rest_framework.response import Response
from rest_framework.views import APIView

import service.integration.bcb


class Historical(APIView):
    def get(self, *args, **kwargs):
        # response = service.integration.bcb.BancoCentralAPI().historical_data_cdi()
        response = service.integration.bcb.BancoCentralAPI().historical_data_selic()

        return Response(response, status=200)
