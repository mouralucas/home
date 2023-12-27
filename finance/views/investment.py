from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import service.finance.investment
from finance.requests.investment import InvestmentGetSerializer, TypeGetSerializer, ProfitGetSerializer, InvestmentPostSerializer
from service.security.security import IsAuthenticated


class Investment(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get investments of the user', parameters=[InvestmentGetSerializer], responses={200: None})
    def get(self, *args, **kwargs):
        validators = InvestmentGetSerializer(data=self.request.query_params)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        investment_id = validators.validated_data.get('investmentId')
        show_mode = validators.validated_data.get('showMode')
        user = self.request.user.id

        response = service.finance.investment.Investment(investment_id=investment_id, owner_id=user).get_investment(show_mode=show_mode)

        return Response(response)

    @extend_schema(summary='Create a new investment', request=InvestmentPostSerializer, responses={200: None})
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

    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint fetches the statement for every investment registered by the user.\n '
                               'It can by filtered by investment and/or period range',
                   parameters=[], responses={501: None})
    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')

        # response = service.finance.investment.Investment(period=period).get_investment_statement()

        return Response({'success': False, 'message': 'This endpoint was not implemented yet'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint create a new entry for a investment for a specific period',
                   request=[], responses={501: None})
    def post(self, *args, **kwargs):
        period = self.request.query_params.get('period')

        return Response({}, status=200)


class Type(APIView):
    @extend_schema(summary='Get investment types', parameters=[TypeGetSerializer], responses={200: None})
    def get(self, *args, **kwargs):
        data = TypeGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        show_mode = data.validated_data.get('show_mode')

        response = service.finance.investment.Investment().get_investment_type(show_mode=show_mode)

        return Response(response)


class Allocation(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get the current investment allocation by investment type', parameters=[], responses={200: None})
    def get(self, *args, **kwargs):
        user = self.request.user.id

        response = service.finance.investment.Investment(owner_id=user).get_allocation()

        return Response(response)


class Interest(APIView):
    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint returns the interest rate based in periodicity and start date',
                   parameters=[], responses={501: None})
    def get(self, *args, **kwargs):
        response = service.finance.investment.Investment().get_interest()

        return Response(response, status=200)


class Profit(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint returns the accumulated profit based in periodicity and start date',
                   parameters=[], responses={501: None})
    def get(self, *args, **kwargs):
        data = ProfitGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        start_at = data.validated_data.get('startAt')
        investment_id = data.validated_data.get('investmentId')
        index_id = data.validated_data.get('indexId')
        user = self.request.user.id

        response = service.finance.investment.Investment(investment_id=investment_id, owner_id=user) \
            .get_profit(start_at=start_at, index_id=index_id)

        return Response(response, status=200)


class InterestAccumulated(APIView):
    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint returns the accumulated interest rate based in periodicity and start date',
                   parameters=[], responses={501: None},
                   deprecated=True)
    def get(self, *args, **kwargs):
        response = service.finance.investment.Investment().get_period_interest_accumulated()

        return Response(response, status=200)
