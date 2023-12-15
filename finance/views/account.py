from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.account
import service.finance.finance
from finance.serializers.account import StatementPostSerializer, StatementGetSerializer, BalancePostSerializer, AccountGetSerializer
from service.security.security import IsAuthenticated


class Account(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Return all accounts of selected type',
        manual_parameters=[
            openapi.Parameter(
                name='accountType', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description=_('Tipo de conta (corrente, PJ, Investimento, etc)'), required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'statusCode': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'accounts': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'accountId': openapi.Schema(type=openapi.TYPE_STRING),
                                    'branch': openapi.Schema(type=openapi.TYPE_STRING),
                                    'number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'openAt': openapi.Schema(type=openapi.TYPE_STRING),
                                    'closeAt': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            ),
                        ),
                    },
                ),
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Acesso proibido",
            ),
        },
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

    def get(self, *args, **kwargs):
        data = StatementGetSerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        period = data.validated_data.get('period')
        account_id = data.validated_data.get('accountId')
        user = self.request.user.id

        response = service.finance.account.Account(owner=user).get_statement(account_id=account_id, period=period)

        return Response(response, status=200)

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
