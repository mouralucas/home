from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import service.finance.credit_card
import service.finance.finance
import util.datetime
from finance.serializers.credit_card import CreditCardBillGetSerializer, BillHistorySerializer, CreditCardBillPostSerializer


class CreditCard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user

        response = service.finance.credit_card.CreditCard().get_credit_card()

        return Response(response)


class Bill(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        validator = CreditCardBillGetSerializer(data=self.request.query_params)
        if not validator.is_valid():
            return Response(validator.errors, status=400)

        bill_id = validator.validated_data.get('credit_card_bill_id', 0)
        period = validator.validated_data.get('period', util.datetime.DateTime().current_period())
        card_id = validator.validated_data.get('credit_card_id')
        user = self.request.user.id

        if card_id in ['', '0']:
            card_id = None

        response = service.finance.credit_card.CreditCard(reference=period, credit_card_id=card_id, owner=user) \
            .get_credit_card_bill(credit_card_bill_id=bill_id)

        return Response(response, status=200)

    def post(self, *args, **kwargs):
        data = CreditCardBillPostSerializer(data=self.request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Criar parâmetro do cadastro do cartão indicando se o cartão gera cashback no formato de investimento, se sim
        # cria uma linha no investimento com a porcentagem pré determinada
        # TODO: padronizar parâmetros como camel case recebidos do front
        # credit_card_bill_id = data.validated_data.get('creditCardBillId')
        # amount = data.validated_data.get('amount')
        # amount_currency = self.request.data.get('amount_currency')
        # price_dollar = self.request.data.get('price_dollar')
        # amount_tax = self.request.data.get('amount_tax')
        # price_currency_dollar = self.request.data.get('price_currency_dollar')
        # dat_purchase = self.request.data.get('purchaseAt')
        # dat_payment = self.request.data.get('paymentAt')
        # installment = self.request.data.get('installment', 1)  # TODO: vira como forma de lista
        # tot_installment = self.request.data.get('installmentTotal', 1)
        # currency_id = self.request.data.get('currency_id', 'BRL')
        # description = self.request.data.get('description')
        # category_id = self.request.data.get('categoryId')
        # card_id = self.request.data.get('creditCardId')
        # cash_flow_id = self.request.data.get('cashFlowId')
        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user) \
            .set_bill(data=data.validated_data,request=self.request)

        return Response(response, status=response['statusCode'])


class BillHistory(APIView):
    def get(self, *args, **kwargs):
        data = BillHistorySerializer(data=self.request.query_params)
        if not data.is_valid():
            return Response(data.errors, status=400)

        start_at = data.validated_data.get('startAt')
        end_at = data.validated_data.get('endAt')
        type = data.validated_data.get('type')
        user = self.request.user.id

        response = service.finance.credit_card.CreditCard(owner=user).get_bill_history(history_type=type, start_at=start_at, end_at=end_at)

        return Response(response, status=200)
