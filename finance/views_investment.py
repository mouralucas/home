from rest_framework.response import Response
from rest_framework.views import APIView

import BO.finance.investment


class Investment(APIView):
    def get(self, *args, **kwargs):
        show_mode = self.request.query_params.get('show_mode')
        investment_id = self.request.query_params.get('investment_id')

        response = BO.finance.investment.Investment(investment_id=investment_id).get_investment(show_mode=show_mode)

        return Response(response)

    def post(self, *args, **kwargs):
        parent_id = self.request.data.get('parentId')
        name = self.request.data.get('name')
        date = self.request.data.get('date')
        quantity = self.request.data.get('quantity')
        price = self.request.data.get('price')
        amount = self.request.data.get('amount')
        cash_flow = self.request.data.get('cashFlow')
        interest_rate = self.request.data.get('interestRate')
        interest_index = self.request.data.get('interestIndex')
        investment_type_id = self.request.data.get('investmentTypeId')
        dat_maturity = self.request.data.get('maturityDate')
        custodian_id = self.request.data.get('custodianId')
        user = self.request.user.id

        response = BO.finance.investment.Investment(parent_id=parent_id, name=name, date=date, quantity=quantity, price=price, amount=amount,
                                                    cash_flow=cash_flow, interest_rate=interest_rate, interest_index=interest_index,
                                                    investment_type_id=investment_type_id, dat_maturity=dat_maturity, custodian_id=custodian_id,
                                                    owner_id=user, request=self.request).set_investment()

        return Response(response)


class InvestmentType(APIView):
    def get(self, *args, **kwargs):
        show_mode = self.request.GET.get('show_mode')

        response = BO.finance.investment.Investment().get_investment_type(show_mode=show_mode)

        return Response(response)


class Proportion(APIView):
    def get(self, *args, **kwargs):
        response = BO.finance.investment.Investment().get_proportion()

        return Response(response)
