from rest_framework.response import Response
from rest_framework.views import APIView

import BO.finance.investment


class Investment(APIView):
    def get(self, *args, **kwargs):
        response = BO.finance.investment.Investment().get_investment()

        return Response(response)

    def post(self, *args, **kwargs):
        pass


class Proportion(APIView):
    def get(self, *args, **kwargs):
        response = BO.finance.investment.Investment().get_proportion()

        return Response(response)
