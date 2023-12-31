from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.account
import service.finance.finance
from core.responses import InvalidRequestError, NotImplementedResponse
from finance.requests.account import StatementPostRequest, StatementGetRequest, BalancePostRequest, AccountGetRequest, AccountPostRequest
from finance.responses.account import AccountGetResponse, StatementGetResponse
from service.security.security import IsAuthenticated


class Account(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get the user accounts.', description='Fetch all accounts registered by the user, based on account type',
        parameters=[AccountGetRequest], responses={200: AccountGetResponse, 400: InvalidRequestError},
    )
    def get(self, *args, **kwargs):
        data = AccountGetRequest(data=self.request.query_params)
        if not data.is_valid():
            pass  # the type is not validated in filter yet
            # return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        is_investment = data.validated_data.get('isInvestment')
        user = self.request.user.id

        response = service.finance.account.Account(owner=user).get_accounts(is_investment=is_investment)

        return Response(response, status=response['statusCode'])

    @extend_schema(summary='Not implemented', description='Create a new account',
                   request=AccountPostRequest, responses={501: NotImplementedResponse})
    def post(self, *args, **kwargs):
        return Response(NotImplementedResponse, status=status.HTTP_501_NOT_IMPLEMENTED)


class Statement(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get statement entries', description='Fetch all entries for an account, if specified. The period can be specified too, if none current period are set',
                   parameters=[StatementGetRequest], responses={200: StatementGetResponse, 400: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = StatementGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors), status=status.HTTP_400_BAD_REQUEST)

        period = data.validated_data.get('period')
        account_id = data.validated_data.get('accountId')
        user = self.request.user.id

        response = service.finance.account.Account(owner=user).get_statement(account_id=account_id, period=period)

        return Response(response, status=200)

    @extend_schema(summary='Create a new statement entry', request=StatementPostRequest, responses={200: None})
    def post(self, *args, **kwargs):
        data = StatementPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        user = self.request.user.id

        response = service.finance.account.Account(owner=user) \
            .set_statement(data=data.validated_data, request=self.request)

        return Response(response, status=200)


class Balance(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get account balance (in test)', parameters=[], responses={200, None})
    def get(self, *args, **kwargs):
        response = service.finance.account.Account(owner=self.request.user.id).get_balance_tests()

        return Response(response)

    @extend_schema(summary='Update user statement (in test)', request=[], responses={200: None})
    def post(self, *args, **kwargs):
        data = BalancePostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        account_id = data.validated_data.get('accountId')

        response = service.finance.account.Account(account_id=account_id).set_balance()

        return Response(response, status=200)
