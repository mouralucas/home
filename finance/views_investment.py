from rest_framework.response import Response
from rest_framework.views import APIView

import BO.finance.investment


class Investment(APIView):
    def get(self, *args, **kwargs):
        investment_id = self.request.query_params.get('investment_id')

        response = BO.finance.investment.Investment(investment_id=investment_id).get_investment()

        return Response(response)

    def post(self, *args, **kwargs):
        pass


class InvestmentType(APIView):
    def get(self, *args, **kwargs):
        show_mode = self.request.GET.get('show_mode')

        response = BO.finance.investment.Investment().get_investment_type(show_mode=show_mode)

        return Response(response)


class Proportion(APIView):
    def get(self, *args, **kwargs):
        response = BO.finance.investment.Investment().get_proportion()

        return Response(response)
