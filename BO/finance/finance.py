import os
from collections import defaultdict
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F, Case, When, BooleanField, CharField, Value
from django.utils.translation import gettext_lazy as _

import core.models
import core.serializers
import finance.models
import finance.serializers
import util.datetime


class Financeiro:

    def __init__(self, mes=None, ano=None, extrato_id=None, fatura_id=None, referencia=None, conta_id=None, cartao_id=None, valor=None,
                 vlr_original=None, vlr_dolar=None, vlr_moeda=None, iof=None, nr_parcela=None, tot_parcela=None, dat_compra=None, dat_pagamento=None,
                 descricao=None, categoria_id=None, currency_id=None):
        self.mes = mes
        self.ano = ano

        self.extrato_id = extrato_id
        self.fatura_id = fatura_id
        self.referencia = referencia
        self.valor = valor
        self.vlr_original = vlr_original
        self.vlr_dolar = vlr_dolar
        self.vlr_moeda = vlr_moeda
        self.iof = iof
        self.nr_parcela = nr_parcela
        self.tot_parcela = tot_parcela
        self.dat_compra = dat_compra
        self.dat_pagamento = dat_pagamento
        self.descricao = descricao
        self.categoria_id = categoria_id
        self.conta_id = conta_id
        self.cartao_id = cartao_id
        self.currency = currency_id

        self.response = {}

    def get_contas(self, selected_id=''):
        contas = finance.models.ContaBancaria.objects.values('nome', 'nm_banco').ativos() \
            .annotate(is_selected=Case(When(nome=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField()))

        self.response['status'] = True
        self.response['contas'] = list(contas)

        return self.response

    def get_cartoes(self, selected_id=''):
        # TODO: mudar para receber parametro de status
        cards = finance.models.CartaoCredito.objects.values('nome', 'nm_descritivo', 'descricao', 'dat_fechamento', 'dat_vencimento').ativos() \
            .annotate(id=F('nome'),
                      nm_status=Case(When(status=True, then=Value('Ativo')),
                                     default=Value('Cancelado'),
                                     output_field=CharField()),
                      is_selected=Case(When(nome=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField())).order_by('-status', 'nome')

        self.response['status'] = True
        self.response['cards'] = list(cards)

        return self.response

    def get_categorias(self, selected_id=''):
        categorias = core.models.Categoria.objects.values('nome', 'descricao').ativos() \
            .annotate(is_selected=Case(When(nome=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField()))

        self.response['status'] = True
        self.response['categorias'] = list(categorias)
        return self.response

    def set_extrato(self, request=None):
        if not self.dat_compra or not self.valor or not self.categoria_id or not self.conta_id:
            self.response['status'] = False
            self.response['descricao'] = 'Todos os parâmetros são obrigatórios'
            return self.response

        if self.extrato_id:
            extrato = finance.models.Extrato.objects.filter(pk=self.extrato_id).first()
        else:
            extrato = finance.models.Extrato()

        dat_compra_date = util.datetime.data_to_datetime(self.dat_compra, formato='%d/%m/%Y')
        referencia_ano = dat_compra_date.year
        referencia_mes = dat_compra_date.month
        self.referencia = referencia_ano * 100 + referencia_mes

        extrato.referencia = self.referencia
        extrato.valor = float(self.valor) * -1
        extrato.dat_compra = dat_compra_date
        extrato.descricao = self.descricao
        extrato.categoria_id = self.categoria_id
        extrato.conta_id = self.conta_id
        extrato.save(request_=request)

    def get_extrato(self):
        filters = {
            'referencia': self.referencia
        }

        if self.conta_id:
            filters['conta_id'] = self.conta_id

        extrato = finance.models.Extrato.objects.values('id', 'referencia', 'dat_compra', 'descricao') \
            .filter(**filters).annotate(total=Sum('valor'),
                                        conta=F('conta__nm_banco')) \
            .order_by('conta_id', 'dat_compra')

        self.response['status'] = True
        self.response['extrato'] = list(extrato)
        return self.response

    def set_bill(self, request=None):
        if not self.dat_compra or not self.valor or not self.categoria_id or not self.cartao_id:
            self.response['status'] = False
            self.response['descricao'] = 'Todos os parâmetros são obrigatórios'
            return self.response

        if self.fatura_id:
            fatura = finance.models.FaturaCredito.objects.filter(pk=self.fatura_id).first()
        else:
            fatura = finance.models.FaturaCredito()

        dat_pagamento_date = util.datetime.data_to_datetime(self.dat_pagamento, formato='%d/%m/%Y')
        referencia_ano = dat_pagamento_date.year
        referencia_mes = dat_pagamento_date.month
        self.referencia = referencia_ano * 100 + referencia_mes

        fatura.cartao_credito_id = self.cartao_id
        fatura.referencia = self.referencia
        fatura.dat_pagamento = dat_pagamento_date
        fatura.dat_compra = util.datetime.data_to_datetime(self.dat_compra, formato='%d/%m/%Y')
        fatura.valor = float(self.valor) * -1
        fatura.categoria_id = self.categoria_id
        fatura.vlr_original = float(self.valor) * -1
        fatura.currency = self.currency
        fatura.nr_parcela = self.nr_parcela
        fatura.tot_parcela = self.tot_parcela
        fatura.descricao = self.descricao
        print(fatura)
        fatura.save(request_=request)

    def get_bills(self):
        filters = {
            'referencia': self.referencia
        }

        if self.cartao_id:
            filters['cartao_credito_id'] = self.cartao_id

        faturas = finance.models.FaturaCredito.objects \
            .values('id', 'referencia', 'dat_compra', 'dat_pagamento',
                    'nr_parcela', 'tot_parcela', 'descricao') \
            .filter(**filters) \
            .annotate(total=Sum('valor'),
                      cartao=F('cartao_credito__nm_descritivo'),
                      nm_categoria=F('categoria__descricao')).order_by('dat_compra')

        self.response['status'] = True
        self.response['faturas'] = list(faturas)
        return self.response
        # return list(faturas)

    def get_evolucao_faturas(self, months=13):
        evolucao = finance.models.FaturaCredito.objects.values('referencia') \
            .filter(referencia__range=(202001, 202112)).annotate(total=Sum('valor'),
                                                                 cartao=F('cartao_credito__nm_descritivo')).order_by('referencia', 'cartao_credito_id')

        evolucao = pd.DataFrame(evolucao)
        saida = evolucao.pivot(index='referencia', columns='cartao', values='total').fillna(0)

        self.response['status'] = True
        self.response['faturas'] = saida.values.tolist()

        return self.response

    def get_evolucao_categoria(self, months=13):
        evolucao_credito = finance.models.FaturaCredito.objects.values('referencia', 'categoria__descricao') \
            .filter(referencia__range=(202001, 202112), categoria__categoriaagrupamento__tipo_agrupamento='gasto_fixo').annotate(total=Sum('valor')).order_by('referencia')

        evolucao_contas = finance.models.Extrato.objects.values('referencia', 'categoria__descricao') \
            .filter(referencia__range=(202001, 202112), categoria__categoriaagrupamento__tipo_agrupamento='gasto_fixo').annotate(total=Sum('valor')).order_by('referencia')

        evolucao = evolucao_contas.union(evolucao_credito)

        default = defaultdict(float)

        for i in list(evolucao):
            default[str(i.get('referencia', '')) + '.' + i.get('categoria__descricao', '')] += float(i.get('total', 0))

        default = [{'referencia': i.split('.')[0], 'categoria': i.split('.')[1], 'total': default[i]} for i in sorted(default)]

        self.response['status'] = True
        self.response['faturas'] = default
        return self.response

    def get_investments(self):
        investments = finance.models.Aplicacao.objects.values('pk', 'nm_descritivo', 'dat_aplicacao', 'vlr_investido', 'preco_aplicacao',
                                                                 'qtd_titulos', 'rent_contratada', 'descricao') \
            .annotate(id=F('pk'),
                      tipo=F('tipo__nm_descritivo'))

        response = {
            'status': True,
            'descricao': None,
            'investments': list(investments)
        }

        return response

    def get_extrato_investimentos(self):
        invest = finance.models.ExtratoAplicacao.objects.values('id', 'vlr_investido', 'vlr_bruto', 'vlr_liquido', 'referencia') \
            .filter(referencia=self.referencia).annotate(nm_investimento=F('aplicacao__nm_descritivo')).order_by('aplicacao__nm_descritivo')

        self.response['status'] = True
        self.response['investimentos'] = list(invest)

        return self.response

    def import_csv_fatura(self, path=None, skiprows=0):
        itens = pd.DataFrame([])

        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)
        self.referencia = name[0].split('-')[1] + name[0].split('-')[2]

        for df in pd.read_csv(path, iterator=True, chunksize=10000, skiprows=skiprows):
            itens = itens.append(pd.DataFrame(df))

        lista_itens_retorno = []
        lista_itens = []
        for index, row in itens.iterrows():
            item = finance.models.FaturaImported()
            item.referencia = self.referencia
            item.data = datetime.strptime(row['date'], '%Y-%m-%d').date()
            item.valor = row['amount']
            item.vlr_original = row['amount']
            item.moeda_codigo = 'real'
            item.is_validado = False
            item.cat_referencia = row['category']
            item.descricao = row['title']
            item.cartao_credito_id = 'nubank'
            lista_itens_retorno.append(finance.serializers.FaturaSerializer(item).data)
            lista_itens.append(item)

        finance.models.FaturaCredito.objects.bulk_create(lista_itens)

        return lista_itens_retorno

    def import_csv_investimento(self, path=None, skiprows=0):
        itens = pd.DataFrame([])

        df = pd.read_excel(path)

        print(df)

        for row in df.head().itertuples():
            print(row)

    def get_payment_date(self, dat_purchase, credit_card_id):
        card = finance.models.CartaoCredito.objects.filter(pk=credit_card_id, status=True).first()

        if not card or not dat_purchase:
            response = {
                'status': False,
                'description': _('Cartão de crédito não válido ou data de compra inválida')
            }
            return response

        day_close = card.dat_fechamento
        day_payment = card.dat_vencimento

        dat_purchase = util.datetime.data_to_datetime(dat_purchase, formato='%d/%m/%Y')
        day_purchase = dat_purchase.day
        month_purchase = dat_purchase.month
        year_purchase = dat_purchase.year

        # TODO: there is a problem when threshold day is in previous month, then the simple rule of >= does not apply
        dat_payment = datetime(day=day_payment, month=month_purchase, year=year_purchase)
        if day_purchase >= day_close:
            dat_payment = dat_payment + relativedelta(months=1)

        response = {
            'status': True,
            'dat_payment': dat_payment.date()
        }
        print(dat_payment.date())
        return response

    def _set_referencia(self):
        dat_compra_date = util.datetime.data_to_datetime(self.dat_compra, formato='%d/%m/%Y')
        referencia_ano = dat_compra_date.year
        referencia_mes = dat_compra_date.month
        self.referencia = referencia_ano * 100 + referencia_mes
