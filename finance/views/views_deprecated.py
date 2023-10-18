from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

import service.core.core
import service.finance.finance
import service.finance.data_import
import service.finance.credit_card
import service.integration.vat_rate
import util.datetime
from service.security.security import IsAuthenticated





class PdfImport(APIView):
    def get(self, *args, **kwargs):
        path = self.request.query_params.get('path')
        period = self.request.query_params.get('period')
        pdf_type = self.request.query_params.get('pdf_origin')

        if pdf_type == 'picpay_statement':
            response = service.finance.finance.Finance().import_picpay_statement(path=path)
        elif pdf_type == 'picpay_bill':
            response = service.finance.finance.Finance().import_picpay_bill(path=path, period=period)
        else:
            response = {
                'status': False,
                'descriptions': _('Não implementado')
            }


        response = {}

        return JsonResponse(response, safe=False)


class ExpensesHistory(View):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        referencia = self.request.GET.get('referencia')

        response = service.finance.finance.Finance(period=referencia).get_category_history()

        return Response(response)


class Expense(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')
        expense_type = self.request.GET.get('expense_type')
        user = self.request.user.id

        response = service.finance.finance.Finance(period=period, owner=user).get_expenses(expense_type=expense_type)

        return JsonResponse(response, safe=False)


class InvestmentStatement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        period = self.request.GET.get('period')

        response = service.finance.finance.Finance(period=period).get_investment_statement()

        return JsonResponse(response, safe=False)

    def post(self, *args, **kwargs):
        period = self.request.query_params.get('period')


class Summary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        # TODO: add serializer
        period = self.request.query_params.get('period', util.datetime.DateTime().current_period())
        user = self.request.user.id

        response = service.finance.finance.Finance(period=period, owner=user).get_summary()

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

        response = service.finance.finance.Finance().import_csv_fatura(
            path='/run/media/lucas/Dados/Projetos/Financeiro/dados_csv/nubank-2021-11.csv')
        # response = service.finance.finance.Financeiro().import_csv_investimento(path='/run/media/lucas/Dados/System/Documents/mega/Financeiro/2021/202106-PreFixado.xlsx')
        return JsonResponse(response, safe=False)





class PaymentDate(View):
    def get(self, *args, **kwargs):
        dat_purchase = self.request.GET.get('dat_purchase')
        credit_card_id = self.request.GET.get('credit_card_id')

        response = service.finance.finance.Finance().get_due_date(dat_purchase=dat_purchase, credit_card_id=credit_card_id)

        return JsonResponse(response, safe=False)


class ImportExcelPagBank(APIView):
    def post(self, *args, **kwargs):
        path = self.request.query_params.get('excel_path', 'C:\\Users\\lucas\\OneDrive\\Financeiro\\Extratos\\Mãe\\Pag-202302.xlsx')

        response = service.finance.data_import.Pagbank(path=path).excel()

        return Response(response)


class Bank(APIView):
    def get(self, *args, **kwargs):
        bank = service.finance.finance.Finance().get_bank()

        return Response(bank)
