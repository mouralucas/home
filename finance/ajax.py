from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView

import BO.core.core
import BO.finance.finance
import util.datetime


class BankAccount(APIView):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id')

        response = BO.finance.finance.Finance().get_bank_accounts(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class CreditCard(APIView):
    def get(self, *args, **kwargs):
        selected_id = self.request.GET.get('selected_id')

        response = BO.finance.finance.Finance().get_credit_cards(selected_id=selected_id)

        return JsonResponse(response, safe=False)


class Statement(APIView):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        reference = self.request.GET.get('referencia')
        conta_id = self.request.GET.get('conta_id')

        if conta_id in ['', '0']:
            conta_id = None

        response = BO.finance.finance.Finance(reference=reference, account_id=conta_id).get_statement()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        extrato_id = self.request.POST.get('extrato_id')
        referencia = self.request.POST.get('referencia')  # não é enviado
        valor = self.request.POST.get('valor')
        dat_compra = self.request.POST.get('dat_compra')
        descricao = self.request.POST.get('descricao')
        categoria_id = self.request.POST.get('categoria_id')
        conta_id = self.request.POST.get('conta_id')

        response = BO.finance.finance.Finance(statement_id=extrato_id, reference=referencia, amount=valor, dat_compra=dat_compra, description=descricao,
                                              categoria_id=categoria_id, account_id=conta_id) \
            .set_extrato(request=self.request)

        return JsonResponse(response, safe=False)


class Bill(APIView):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        referencia = self.request.GET.get('anomes', util.datetime.DateTime().current_period())
        card_id = self.request.GET.get('card')

        if card_id in ['', '0']:
            card_id = None

        response = BO.finance.finance.Finance(reference=referencia, credit_card_id=card_id).get_bills()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        bill_id = self.request.POST.get('fatura_id')
        price = self.request.POST.get('valor')
        vlr_dolar = self.request.POST.get('vlr_dolar')
        dat_purchase = self.request.POST.get('dat_compra')
        dat_payment = self.request.POST.get('dat_pagamento')
        nr_parcela = self.request.POST.get('nr_parcela', 1)
        tot_parcela = self.request.POST.get('tot_parcela', 1)
        currency = self.request.POST.get('currency')
        descricao = self.request.POST.get('descricao')
        categoria_id = self.request.POST.get('categoria_id')
        cartao_id = self.request.POST.get('cartao_id')

        response = BO.finance.finance.Finance(bill_id=bill_id, amount=price, vlr_dolar=vlr_dolar, dat_compra=dat_purchase, dat_pagamento=dat_payment,
                                              nr_parcela=nr_parcela, tot_parcela=tot_parcela, currency_id=currency, description=descricao,
                                              categoria_id=categoria_id, credit_card_id=cartao_id) \
            .set_bill(request=self.request)

        return JsonResponse(response, safe=False)


class ExpensesEvolution(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        referencia = self.request.GET.get('referencia')

        response = BO.finance.finance.Finance(reference=referencia).get_evolucao_categoria()

        return JsonResponse(response, safe=False)


class FixedExpenses(View):
    def get(self, *args, **kwargs):
        reference = self.request.GET.get('reference')

        response = BO.finance.finance.Finance(reference=reference).get_fixed_expenses()

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


