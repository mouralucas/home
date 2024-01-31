from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.account
import service.finance.finance
from base.responses import InvalidRequestError, NotImplementedResponse
from finance.requests.account import StatementPostRequest, StatementGetRequest, BalancePostRequest, AccountGetRequest, AccountPostRequest, BalanceGetRequest
from finance.responses.account import AccountGetResponse, StatementGetResponse, StatementPostResponse, BalanceGetResponse, AccountPostResponse
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

    @extend_schema(summary='Create a new account', description='Create a new account for the logged user',
                   request=AccountPostRequest, responses={201: AccountPostResponse, 400: InvalidRequestError})
    def post(self, *args, **kwargs):
        data = AccountPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user.id

        response = service.finance.account.Account(request=self.request, owner=user).set_account(account=data)

        return Response(response, status=response['statusCode'])


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

    @extend_schema(summary='Create a new statement entry', request=StatementPostRequest, responses={201: StatementPostResponse, 400: InvalidRequestError})
    def post(self, *args, **kwargs):
        data = StatementPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        user = self.request.user.id

        response = service.finance.account.Account(owner=user) \
            .set_statement(data=data.validated_data, request=self.request)

        return Response(response, status=response['statusCode'])


class Balance(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get account balance (in test)', parameters=[], responses={200: BalanceGetResponse})
    def get(self, *args, **kwargs):
        response = service.finance.account.Account(owner=self.request.user.id).get_balance_tests()

        return Response(response)

    @extend_schema(summary='Update user balance (in test)',
                   request=BalancePostRequest, responses={200: None, 400: InvalidRequestError})
    def post(self, *args, **kwargs):
        data = BalancePostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=400)

        account_id = data.validated_data.get('accountId')

        response = service.finance.account.Account().set_balance(account_id=account_id)

        return Response(response, status=200)
