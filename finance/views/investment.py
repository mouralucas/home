from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.investment
from finance.serializers.investment import InvestmentGetSerializer, InvestmentPostSerializer
from service.security.security import IsAuthenticated


class Investment(APIView):
    def get(self, *args, **kwargs):
        validators = InvestmentGetSerializer(data=self.request.query_params)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        investment_id = validators.validated_data.get('investmentId')
        show_mode = validators.validated_data.get('showMode')

        response = service.finance.investment.Investment(investment_id=investment_id).get_investment(show_mode=show_mode)

        return Response(response)

    def post(self, *args, **kwargs):
        validators = InvestmentPostSerializer(data=self.request.data)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        parent_id = validators.validated_data.get('parentId')
        name = validators.validated_data.get('name')
        date = validators.validated_data.get('date')
        quantity = validators.validated_data.get('quantity')
        price = validators.validated_data.get('price')
        amount = validators.validated_data.get('amount')
        cash_flow = validators.validated_data.get('cashFlowId')
        interest_rate = validators.validated_data.get('interestRate')
        interest_index = validators.validated_data.get('interestIndex')
        investment_type_id = validators.validated_data.get('investmentTypeId')
        dat_maturity = validators.validated_data.get('maturityDate')
        custodian_id = validators.validated_data.get('custodianId')
        user = self.request.user.id

        response = service.finance.investment.Investment(parent_id=parent_id, name=name, date=date, quantity=quantity, price=price, amount=amount,
                                                         cash_flow=cash_flow, interest_rate=interest_rate, interest_index=interest_index,
                                                         investment_type_id=investment_type_id, dat_maturity=dat_maturity, custodian_id=custodian_id,
                                                         owner_id=user, request=self.request).set_investment()

        return Response(response)


class Statement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')

        response = service.finance.investment.Investment(reference=period).get_investment_statement()

        return Response(response, status=200)

    def post(self, *args, **kwargs):
        period = self.request.query_params.get('period')

        return Response({}, status=200)


class InvestmentType(APIView):
    def get(self, *args, **kwargs):
        validators = InvestmentGetSerializer(data=self.request.query_params)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        show_mode = validators.validated_data.get('show_mode')

        response = service.finance.investment.Investment().get_investment_type(show_mode=show_mode)

        return Response(response)


class Proportion(APIView):
    def get(self, *args, **kwargs):
        response = service.finance.investment.Investment().get_proportion()

        return Response(response)


class Interest(APIView):
    def get(self, *args, **kwargs):
        response = service.finance.investment.Investment().get_interest()

        return Response(response, status=200)


class Profit(APIView):
    def get(self, *args, **kwargs):
        Response({}, status=False)


class InterestAccumulated(APIView):
    def get(self, *args, **kwargs):
        response = service.finance.investment.Investment().get_period_interest_accumulated()

        return Response(response, status=200)
