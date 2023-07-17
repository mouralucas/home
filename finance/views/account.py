from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.account
import service.finance.finance
from service.security.security import IsAuthenticated
from finance.serializers.account import AccountStatementPostSerializer, AccountStatementGetSerializer


class Account(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user.id

        response = service.finance.account.Account(owner=user).get_accounts()

        return Response(response)


class AccountStatement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        validators = AccountStatementGetSerializer(data=self.request.query_params)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        reference = validators.validated_data.get('reference')
        account_id = validators.validated_data.get('accountId')
        user = self.request.user.id

        if account_id in ['', '0']:
            account_id = None

        response = service.finance.finance.Finance(reference=reference, account_id=account_id, owner=user).get_statement()

        return Response(response, status=200)

    def post(self, *args, **kwargs):
        validators = AccountStatementPostSerializer(data=self.request.data)
        if not validators.is_valid():
            return Response(validators.errors, status=400)

        statement_id = validators.validated_data.get('statementId')
        amount = validators.validated_data.get('amount')
        dat_purchase = validators.validated_data.get('purchasedAt')
        description = validators.validated_data.get('description')
        category_id = validators.validated_data.get('categoryId')
        account_id = validators.validated_data.get('accountId')
        currency_id = validators.validated_data.get('currencyId')
        cash_flow_id = validators.validated_data.get('cashFlowId')
        user = self.request.user.id

        response = service.finance.finance.Finance(statement_id=statement_id, amount=amount, dat_compra=dat_purchase,
                                                   description=description,
                                                   category_id=category_id, account_id=account_id, currency_id=currency_id,
                                                   cash_flow_id=cash_flow_id, owner=user) \
            .set_statement(request=self.request)

        return Response(response, status=200)
