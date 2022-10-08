from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView

import BO.core.core
import BO.finance.finance

import util.datetime
from django.utils.translation import gettext_lazy as _


class BankAccount(APIView):
    def get(self, *args, **kwargs):
        response = BO.finance.finance.Finance().get_bank_accounts()

        return JsonResponse(response, safe=False)


class CreditCard(APIView):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id')

        response = BO.finance.finance.Finance().get_credit_cards()

        return JsonResponse(response, safe=False)


class Statement(APIView):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        period = self.request.GET.get('reference')
        account_id = self.request.GET.get('account_id')

        if account_id in ['', '0']:
            account_id = None

        response = BO.finance.finance.Finance(period=period, account_id=account_id).get_statement()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        statement_id = self.request.POST.get('statement_id')
        amount = self.request.POST.get('amount')
        dat_purchase = self.request.POST.get('dat_purchase')
        description = self.request.POST.get('description')
        category_id = self.request.POST.get('category_id')
        account_id = self.request.POST.get('account_id')

        response = BO.finance.finance.Finance(statement_id=statement_id, amount=amount, dat_compra=dat_purchase, description=description,
                                              category_id=category_id, account_id=account_id) \
            .set_statement(request=self.request)

        return JsonResponse(response, safe=False)


class PdfImport(APIView):
    def post(self, *args, **kwargs):
        path = self.request.POST.get('path')
        pdf_type = self.request.POST.get('pdf_origin')

        if pdf_type == 'picpay_statement':
            response = BO.finance.finance.Finance().import_picpay_statement(path=path)
        else:
            response = {
                'status': False,
                'descriptions': _('Não implementado')
            }

        return JsonResponse(response, safe=False)


class Bill(APIView):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        bill_id = self.request.GET.get('credit_card_bill_id', 0)
        referencia = self.request.GET.get('reference', util.datetime.DateTime().current_period())
        card_id = self.request.GET.get('card')

        if card_id in ['', '0']:
            card_id = None

        response = BO.finance.finance.Finance(period=referencia, credit_card_id=card_id).get_bill(credit_card_bill_id=bill_id)

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        bill_id = self.request.POST.get('fatura_id')
        amount = self.request.POST.get('amount')
        amount_currency = self.request.POST.get('amount_currency')
        price_dollar = self.request.POST.get('price_dollar')
        amount_tax = self.request.POST.get('amount_tax')
        price_currency_dollar = self.request.POST.get('price_currency_dollar')
        dat_purchase = self.request.POST.get('dat_purchase')
        dat_payment = self.request.POST.get('dat_payment')
        stallment = self.request.POST.get('stallment', 1)  # TODO: vira como forma de lista
        tot_stallment = self.request.POST.get('tot_stallment', 1)
        currency = self.request.POST.get('currency')
        description = self.request.POST.get('description')
        category_id = self.request.POST.get('category_id')
        card_id = self.request.POST.get('card_id')

        response = BO.finance.finance.Finance(bill_id=bill_id, amount=amount, amount_currency=amount_currency, price_currency_dollar=price_currency_dollar, price_dollar=price_dollar,
                                              dat_compra=dat_purchase, dat_pagamento=dat_payment, amount_tax=amount_tax,
                                              installment=stallment, tot_installment=tot_stallment, currency_id=currency, description=description,
                                              category_id=category_id, credit_card_id=card_id) \
            .set_bill(request=self.request)

        return JsonResponse(response, safe=False)


class ExpensesHistory(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        referencia = self.request.GET.get('referencia')

        response = BO.finance.finance.Finance(period=referencia).get_evolucao_categoria()

        return JsonResponse(response, safe=False)


class Expense(APIView):
    def get(self, *args, **kwargs):
        reference = self.request.GET.get('reference')
        expense_type = self.request.GET.get('expense_type')

        response = BO.finance.finance.Finance(period=reference).get_expenses(expense_type=expense_type)

        return JsonResponse(response, safe=False)


class FixedExpenses(View):
    def get(self, *args, **kwargs):
        reference = self.request.GET.get('reference')

        response = BO.finance.finance.Finance(period=reference).get_expenses(expense_type='fixed')

        return JsonResponse(response, safe=False)


class VariableExpenses(View):
    def get(self, *args, **kwargs):
        reference = self.request.GET.get('reference')

        response = BO.finance.finance.Finance(period=reference).get_expenses(expense_type='variable')

        return JsonResponse(response, safe=False)


class Investment(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        referencia = self.request.GET.get('referencia')

        response = BO.finance.finance.Finance().get_investments()

        return JsonResponse(response, safe=False)


class Csv(APIView):
    def get(self, *args, **kwargs):
        path = self.request.POST.get('pah')

        response = BO.finance.finance.Finance().import_csv_fatura(path='/run/media/lucas/Dados/Projetos/Financeiro/dados_csv/nubank-2021-11.csv')
        # response = BO.finance.finance.Financeiro().import_csv_investimento(path='/run/media/lucas/Dados/System/Documents/mega/Financeiro/2021/202106-PreFixado.xlsx')
        return JsonResponse(response, safe=False)


class Periodos(APIView):
    def get(self, *args, **kwargs):
        periods = util.datetime.DateTime().list_period()

        return JsonResponse(periods, safe=False)


class Currency(APIView):
    def get(self, *args, **kwargs):
        response = BO.core.core.Misc().get_currency()

        return JsonResponse(response, safe=False)


class PaymentDate(View):
    def get(self, *args, **kwargs):
        dat_purchase = self.request.GET.get('dat_purchase')
        credit_card_id = self.request.GET.get('credit_card_id')

        response = BO.finance.finance.Finance().get_payment_date(dat_purchase=dat_purchase, credit_card_id=credit_card_id)

        return JsonResponse(response, safe=False)
