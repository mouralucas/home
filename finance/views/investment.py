from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import service.finance.investment
from base.responses import NotImplementedResponse, InvalidRequestError
from finance.requests.investment import InvestmentGetRequest, TypeGetRequest, ProfitGetRequest, InvestmentPostRequest, StatementGetRequest, StatementPostRequest, AllocationGetRequest
from finance.responses.investment import StatementGetResponse, StatementPostResponse, TypeGetResponse, AllocationGetResponse
from service.security.security import IsAuthenticated


class Investment(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get investments of the user', parameters=[InvestmentGetRequest], responses={200: None})
    def get(self, *args, **kwargs):
        validators = InvestmentGetRequest(data=self.request.query_params)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        investment_id = validators.validated_data.get('investmentId')
        show_mode = validators.validated_data.get('showMode')
        user = self.request.user.id

        response = service.finance.investment.Investment(investment_id=investment_id, owner_id=user).get_investment(show_mode=show_mode)

        return Response(response)

    @extend_schema(summary='Create a new investment', request=InvestmentPostRequest, responses={200: None})
    def post(self, *args, **kwargs):
        validators = InvestmentPostRequest(data=self.request.data)
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
                   parameters=[StatementGetRequest],
                   responses={200: StatementGetResponse, 400: InvalidRequestError, 501: NotImplementedResponse})
    def get(self, *args, **kwargs):
        data = StatementGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        return Response(NotImplementedResponse({}).data, status=status.HTTP_501_NOT_IMPLEMENTED)

    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint create a new entry for a investment for a specific period',
                   request=StatementPostRequest,
                   responses={200: StatementPostResponse, 400: InvalidRequestError, 501: NotImplementedResponse})
    def post(self, *args, **kwargs):
        data = StatementPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        investment_id = data.validated_data.get('investmentId')
        period = data.validated_data.get('period')

        return Response(NotImplementedResponse({}).data, status=200)


class Type(APIView):
    @extend_schema(summary='Get investment types',
                   parameters=[TypeGetRequest], responses={200: TypeGetResponse, 400: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = TypeGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        show_mode = data.validated_data.get('show_mode')

        response = service.finance.investment.Investment().get_investment_type(show_mode=show_mode)

        return Response(response, status=response['statusCode'])


class Allocation(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get the current investment allocation by investment type',
                   parameters=[AllocationGetRequest], responses={200: AllocationGetResponse, 400: InvalidRequestError})
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
                   parameters=[ProfitGetRequest], responses={400: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = ProfitGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        start_at = data.validated_data.get('startAt')
        investment_id = data.validated_data.get('investmentId')
        index_id = data.validated_data.get('indexId')
        user = self.request.user.id

        response = service.finance.investment.Investment(investment_id=investment_id, owner_id=user) \
            .get_profit(start_at=start_at, index_id=index_id)

        return Response(response, status=response['statusCode'])


class InterestAccumulated(APIView):
    @extend_schema(summary='This endpoint was not implemented yet',
                   description='This endpoint returns the accumulated interest rate based in periodicity and start date',
                   parameters=[], responses={501: None},
                   deprecated=True)
    def get(self, *args, **kwargs):
        response = service.finance.investment.Investment().get_period_interest_accumulated()

        return Response(response, status=200)
