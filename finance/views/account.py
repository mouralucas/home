from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.account
import service.finance.finance
from finance.serializers.account import StatementPostSerializer, StatementGetSerializer, BalancePostSerializer, AccountGetSerializer
from service.security.security import IsAuthenticated


class Account(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[AccountGetSerializer],
        responses={200: None},
    )
    def get(self, *args, **kwargs):
        data = AccountGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        is_investment = data.validated_data.get('isInvestment')
        user = self.request.user.id

        response = service.finance.account.Account(owner=user).get_accounts(is_investment=is_investment)

        return Response(response, status=response['statusCode'])


class Statement(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[StatementGetSerializer], responses={200: None})
    def get(self, *args, **kwargs):
        data = StatementGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        period = data.validated_data.get('period')
        account_id = data.validated_data.get('accountId')
        user = self.request.user.id

        response = service.finance.account.Account(owner=user).get_statement(account_id=account_id, period=period)

        return Response(response, status=200)

    @extend_schema(request=StatementPostSerializer, responses={200: None})
    def post(self, *args, **kwargs):
        data = StatementPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        user = self.request.user.id

        response = service.finance.account.Account(owner=user) \
            .set_statement(data=data.validated_data, request=self.request)

        return Response(response, status=200)


class Balance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        response = service.finance.account.Account(owner=self.request.user.id).get_balance_tests()

        return Response(response)

    def post(self, *args, **kwargs):
        data = BalancePostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        account_id = data.validated_data.get('accountId')

        response = service.finance.account.Account(account_id=account_id).set_balance()

        return Response(response, status=200)
