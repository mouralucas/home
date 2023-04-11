from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import BO.finance.finance
import BO.finance.credit_card
import util.datetime


class CreditCard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        response = BO.finance.credit_card.CreditCard().get_credit_card()

        return Response(response)


class CreditCardBill(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        bill_id = self.request.GET.get('credit_card_bill_id', 0)
        period = self.request.GET.get('period', util.datetime.DateTime().current_period())
        card_id = self.request.GET.get('credit_card_id')
        user = self.request.user.id

        if card_id in ['', '0']:
            card_id = None

        response = BO.finance.credit_card.CreditCard(period=period, credit_card_id=card_id, owner=user) \
            .get_bill(credit_card_bill_id=bill_id)

        return Response(response)

    def post(self, *args, **kwargs):
        bill_id = self.request.POST.get('fatura_id')
        amount = self.request.POST.get('amount')
        amount_currency = self.request.POST.get('amount_currency')
        price_dollar = self.request.POST.get('price_dollar')
        amount_tax = self.request.POST.get('amount_tax')
        price_currency_dollar = self.request.POST.get('price_currency_dollar')
        dat_purchase = self.request.POST.get('dat_purchase')
        dat_payment = self.request.POST.get('dat_payment')
        installment = self.request.POST.get('installment', 1)  # TODO: vira como forma de lista
        tot_installment = self.request.POST.get('tot_installment', 1)
        currency = self.request.POST.get('currency')
        description = self.request.POST.get('description')
        category_id = self.request.POST.get('category_id')
        card_id = self.request.POST.get('card_id')
        cash_flow_id = self.request.POST.get('cashFlowId')
        user = self.request.user.id

        # TODO: migrate to new credit_card BO
        response = BO.finance.finance.Finance(bill_id=bill_id, amount=amount, amount_currency=amount_currency,
                                              price_currency_dollar=price_currency_dollar, price_dollar=price_dollar,
                                              dat_compra=dat_purchase, dat_pagamento=dat_payment, amount_tax=amount_tax,
                                              installment=installment, tot_installment=tot_installment,
                                              currency_id=currency, description=description,
                                              category_id=category_id, credit_card_id=card_id,
                                              cash_flow_id=cash_flow_id, owner=user) \
            .set_bill(request=self.request)

        return Response(response)
