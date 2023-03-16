from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

import BO.core.core
import BO.finance.finance
import BO.integration.vat_rate
import util.datetime
from BO.security.security import IsAuthenticated


class BankAccount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        response = BO.finance.finance.Finance().get_bank_accounts()

        return JsonResponse(response, safe=False)


class CreditCard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id')

        response = BO.finance.finance.Finance().get_credit_cards()

        return JsonResponse(response, safe=False)


class BankStatement(APIView):
    permission_classes = [IsAuthenticated]

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
        currency_id = self.request.POST.get('currencyId')
        cash_flow_id = self.request.POST.get('cashFlowId')

        response = BO.finance.finance.Finance(statement_id=statement_id, amount=amount, dat_compra=dat_purchase,
                                              description=description,
                                              category_id=category_id, account_id=account_id, currency_id=currency_id,
                                              cash_flow_id=cash_flow_id) \
            .set_statement(request=self.request)

        return JsonResponse(response, safe=False)


class PdfImport(APIView):
    def post(self, *args, **kwargs):
        path = self.request.POST.get('path')
        period = self.request.POST.get('period')
        pdf_type = self.request.POST.get('pdf_origin')

        if pdf_type == 'picpay_statement':
            response = BO.finance.finance.Finance().import_picpay_statement(path=path)
        elif pdf_type == 'picpay_bill':
            response = BO.finance.finance.Finance().import_picpay_bill(path=path, period=period)

        else:
            response = {
                'status': False,
                'descriptions': _('Não implementado')
            }

        return JsonResponse(response, safe=False)


class CreditCardBill(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        bill_id = self.request.GET.get('credit_card_bill_id', 0)
        period = self.request.GET.get('period', util.datetime.DateTime().current_period())
        card_id = self.request.GET.get('credit_card_id')

        if card_id in ['', '0']:
            card_id = None

        response = BO.finance.finance.Finance(period=period, credit_card_id=card_id).get_bill(
            credit_card_bill_id=bill_id)

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
        installment = self.request.POST.get('installment', 1)  # TODO: vira como forma de lista
        tot_installment = self.request.POST.get('tot_installment', 1)
        currency = self.request.POST.get('currency')
        description = self.request.POST.get('description')
        category_id = self.request.POST.get('category_id')
        card_id = self.request.POST.get('card_id')
        cash_flow_id = self.request.POST.get('cashFlowId')

        response = BO.finance.finance.Finance(bill_id=bill_id, amount=amount, amount_currency=amount_currency,
                                              price_currency_dollar=price_currency_dollar, price_dollar=price_dollar,
                                              dat_compra=dat_purchase, dat_pagamento=dat_payment, amount_tax=amount_tax,
                                              installment=installment, tot_installment=tot_installment,
                                              currency_id=currency, description=description,
                                              category_id=category_id, credit_card_id=card_id,
                                              cash_flow_id=cash_flow_id) \
            .set_bill(request=self.request)

        return JsonResponse(response, safe=False)


class ExpensesHistory(View):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        referencia = self.request.GET.get('referencia')

        response = BO.finance.finance.Finance(period=referencia).get_category_history()

        return Response(response)


class Expense(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')
        expense_type = self.request.GET.get('expense_type')

        response = BO.finance.finance.Finance(period=period).get_expenses(expense_type=expense_type)

        return JsonResponse(response, safe=False)


class ExpenseCategory(APIView):
    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')

        response = BO.finance.finance.Finance(period=period).get_category_expense()

        return Response(response)


class BillHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period_start = self.request.query_params.get('periodStart')
        period_end = self.request.query_params.get('periodEnd')
        months = self.request.query_params.get('months')

        response = BO.finance.finance.Finance().get_bill_history(period_start=period_start, period_end=period_end)

        return JsonResponse(response, safe=False)


class Investment(View):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        response = BO.finance.finance.Finance().get_investment()

        return JsonResponse(response, safe=False)


class InvestmentStatement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')

        response = BO.finance.finance.Finance(period=period).get_investment_statement()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        period = self.request.query_params.get('period')


class Summary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period = self.request.query_params.get('period', 202301)

        response = BO.finance.finance.Finance(period=period).get_summary()

        return Response(response)


class InvestmentStatementUpload(View):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        #  1º criar upload do arquivo na pasta de arquivos
        #  2º pegar response do upload e ler arquivo e salvar dados
        #  3º Criar tabela para log de arquivos com dados cadastrados ou com possíveis erros
        #       (que sabe mostrar em uma tabela os dados importados e esperar o ok do usuário)
        response = None

        return JsonResponse(response, safe=False)


class Csv(APIView):
    def get(self, *args, **kwargs):
        path = self.request.POST.get('pah')

        response = BO.finance.finance.Finance().import_csv_fatura(
            path='/run/media/lucas/Dados/Projetos/Financeiro/dados_csv/nubank-2021-11.csv')
        # response = BO.finance.finance.Financeiro().import_csv_investimento(path='/run/media/lucas/Dados/System/Documents/mega/Financeiro/2021/202106-PreFixado.xlsx')
        return JsonResponse(response, safe=False)


class Currency(APIView):
    def get(self, *args, **kwargs):
        # response = BO.core.core.Misc().get_currency()
        response = BO.finance.finance.Finance().get_currency()
        # response = BO.integration.vat_rate.Vat().get_currency()

        return JsonResponse(response, safe=False)


class PaymentDate(View):
    def get(self, *args, **kwargs):
        dat_purchase = self.request.GET.get('dat_purchase')
        credit_card_id = self.request.GET.get('credit_card_id')

        response = BO.finance.finance.Finance().get_due_date(dat_purchase=dat_purchase, credit_card_id=credit_card_id)

        return JsonResponse(response, safe=False)
