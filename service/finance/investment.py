import decimal
import json
import warnings
from django.utils.translation import gettext_lazy as _

import pandas as pd
from django.db.models import F, Sum
from rest_framework import status

import finance.models
from finance.requests.investment import GoalPostRequest
from finance.responses.investment import TypeGetResponse, GoalPostResponse
from service.finance.finance import Finance
from django.utils import timezone


class Investment(Finance):
    def __init__(self, investment_id=None, parent_id=None, name=None, date=None, quantity=None, price=None, amount=None, cash_flow=None, interest_rate=None, interest_index=None, investment_type_id=None, dat_maturity=None, custodian_id=None,
                 owner_id=None, period=None, request=None):
        super().__init__(period=period, amount=amount, request=request)

        # TODO: clean code with parent class
        self.investment_id = investment_id
        self.parent_id = parent_id
        self.name = name
        self.date = date
        self.quantity = quantity
        self.price = price
        self.cash_flow = cash_flow
        self.interest_rate = interest_rate
        self.interest_index = interest_index
        self.type_id = investment_type_id
        self.dat_maturity = dat_maturity
        self.custodian_id = custodian_id
        self.owner_id = owner_id


    def set_investment(self):
        # Rewrite this method
        # TODO: Need to include missing parameters that are hard coded rn, like index_id and liquidity_id
        # The Investment serializer are created, but need to check it all fields are mapped
        self.amount = decimal.Decimal(self.amount) * -1 if self.cash_flow == 'OUTGOING' else self.amount

        investment = self.__set_investment()
        investment.save(request_=self.request)

        response = {
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'investment': {
                'investmentId': investment.pk
            }
        }
        return response

    def get_investment(self, show_mode):
        filters = {
            'owner_id': self.owner_id,
            # 'maturity_at__gte': timezone.now()
            'is_liquidated': False
        }

        if show_mode != 'all':
            filters['parent_id__isnull'] = True if show_mode == 'father' else False

        if self.investment_id:
            filters['pk'] = self.investment_id

        investments = finance.models.Investment.objects.values('name', 'description', 'amount', 'price', 'quantity', 'date') \
            .annotate(
            investmentId=F('pk'),
            maturityAt=F('maturity_at'),
            interestRate=F('interest_rate'),
            interestIndex=F('interest_index'),
            currencyId=F('currency_id'),
            currencySymbol=F('currency__symbol'),
            custodianName=F('custodian__name'),
            custodianId=F('custodian_id'),
            investmentTypeId=F('type_id'),
            investmentTypeName=F('type__name'),
            parentId=F('parent_id')
        ).order_by('-date').active().filter(**filters)

        response = {
            'success': True,
            'description': None,
            'quantity': len(investments),
            'isSingleResult': False if not self.investment_id else True,
            'investment': list(investments) if not self.investment_id else investments.first()
        }

        return response

    def get_investment_statement(self):
        statement = finance.models.AccountStatement.objects.all()

        response = {
            'success': True,
        }

        return response

    def get_investment_type(self, show_mode):
        filters = {}

        if show_mode != 'all':
            filters['parent_id__isnull'] = True if show_mode == 'father' else False

        investment_type = (finance.models.InvestmentType.objects.values('description')
                           .annotate(investmentTypeId=F('id'),
                                     investmentTypeName=F('name'),
                                     parentId=F('parent_id'),
                                     parentName=F('parent__name'))
                           .filter(**filters).order_by('name'))

        response = TypeGetResponse({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(investment_type),
            'investmentTypes': investment_type
        }).data

        return response

    def get_allocation(self):
        filters = {
            'owner_id': self.owner_id,
            'is_liquidated': False
        }

        allocation = (finance.models.Investment.objects.values('id', 'amount')
                      .annotate(incomeType=F('type__parent__name'),
                                investmentType=F('type__name'))
                      .filter(**filters).exclude(parent__id__isnull=False))
        income = allocation.values('incomeType').annotate(total=Sum('amount'))
        investment = allocation.values('investmentType').annotate(total=Sum('amount'))

        response = {
            'success': True,
            'incomeAllocation': list(income),
            'investmentAllocation': list(investment)
        }

        return response

    def get_interest(self):
        interest = finance.models.FinanceData.objects \
            .filter(periodicity='dc5b3bf8-2b84-423a-9a90-e7e194e355fa', type_id='2a2b100f-17d9-4c61-b3b4-f06662113953', date__gte='2023-01-01')

        interest_list = interest.values('id') \
            .annotate(date=F('date'),
                      value=F('value'),
                      typeId=F('type_id'),
                      typeName=F('type__name'),
                      unit=F('unit')).order_by('date')

        result = []
        for data_point in list(interest_list):
            date = data_point['date']
            value = float(data_point['value'])
            type_name = str(data_point['typeId'])

            found_entry = next((entry for entry in result if entry['date'] == date), None)
            if found_entry:
                found_entry[type_name] = value
            else:
                new_entry = {'date': date, type_name: value}
                result.append(new_entry)

        accumulated_values = {}
        for data_entry in result:
            date = data_entry["date"]
            for key, value in data_entry.items():
                if key != "date":
                    accumulated_values.setdefault(key, 1.0)  # Inicializa o acumulado com 1.0 (sem acumulação) se não existir
                    accumulated_values[key] *= (1 + value / 100)

        types = interest.values('id') \
            .annotate(value=F('type_id'), name=F('type__name')).distinct('type_id')

        response = {
            'data': result,
            'series': list(types)
        }

        return response

    def get_period_interest_accumulated(self):
        warnings.warn('Função depreciada.', DeprecationWarning, stacklevel=2)
        data = pd.DataFrame(finance.models.FinanceData.objects.values('date', 'value').filter(type_id='2a2b100f-17d9-4c61-b3b4-f06662113953',
                                                                                              periodicity='b9f83ad5-7701-4098-bdaf-ee092f3247eb',
                                                                                              date__gte='2023-08-01'))

        # Certificar-se de que a coluna 'data' está em formato de data
        data['date'] = pd.to_datetime(data['date'])

        # Ordenar o dataset por data
        data = data.sort_values(by='date')
        data['value'] = data['value'].astype(float)
        # Inicializar a taxa de juros acumulada
        taxa_acumulada = 1.0
        taxas_acumuladas = []

        # Iterar sobre as linhas do dataset
        for index, row in data.iterrows():
            taxa_diaria = 1 + row['value'] / 100  # Convertendo a taxa para decimal
            taxa_acumulada *= taxa_diaria
            taxas_acumuladas.append((taxa_acumulada - 1) * 100)

        data['taxa_acumulada'] = taxas_acumuladas

        response = json.loads(data.to_json(orient='records', date_format='iso'))

        return response

    def get_profit(self, start_at, index_id=None):
        if index_id:
            index = finance.models.Index.objects.filter(pk=index_id).first()
        else:
            index = finance.models.Index.objects.filter(pk='2a2b100f-17d9-4c61-b3b4-f06662113953').first()

        statement_filters = {
            'investment__owner_id': self.owner_id,
            'period__gte': start_at
        }

        index_filters = {
            'index': index,
            'periodicity_id': 'dc5b3bf8-2b84-423a-9a90-e7e194e355fa',
            'period__gte': start_at
        }

        investment_name = 'Total'
        if self.investment_id:
            investment_name = finance.models.Investment.objects.values_list('name', flat=True).filter(pk=self.investment_id).first()
            statement_filters['investment_id'] = self.investment_id

        if index_id:
            index_filters['index_id'] = index_id

        # O valor de ganhos no mês devem ser somados ao investido, para não distorcer a % de ganho
        statement = pd.DataFrame(finance.models.InvestmentStatement.objects.values('period').annotate(total=Sum('gross_amount'))
                                 .filter(**statement_filters).order_by('period'))
        if statement.empty:
            statement = pd.DataFrame(columns=['period', 'total'])
        statement['variation_percentage'] = statement['total'].pct_change()
        statement = statement.fillna(0)
        statement['investment'] = (((1 + statement['variation_percentage']).cumprod()) - 1) * 100

        reference_index = pd.DataFrame(finance.models.FinanceData.objects.values('period', 'value').filter(**index_filters).order_by('period'))
        if reference_index.empty:
            reference_index = pd.DataFrame(columns=['period', 'value'])
        reference_index["value"] = reference_index["value"].astype(float)
        # Clean first month, so begins at zero
        if not reference_index.empty:
            reference_index.at[0, "value"] = 0
        reference_index['index'] = ((1 + reference_index['value'] / 100).cumprod() - 1) * 100

        merged_ = statement.merge(reference_index, on='period', how='outer')
        merged_ = merged_.fillna(0)
        merged_ = merged_.sort_values(by='period')

        response_list = []
        for idx, i in merged_.iterrows():
            aux = {
                'reference': str(i['period']),
                'investment': i['investment'],
                'index': i['index']
            }
            response_list.append(aux)

        response = {
            'success': True,
            'data': response_list,
            'series': [
                {
                    'value': 'investment',
                    'name': investment_name
                },
                {
                    'value': 'index',
                    'name': index.name
                }
            ]
        }

        return response

    def get_goals(self):
        pass

    def set_goals(self, goals: GoalPostRequest):
        new_goal = finance.models.InvestmentGoal()

        new_goal.owner_id = self.request.user.id
        new_goal.name = goals.validated_data.get('name')
        new_goal.description = goals.validated_data.get('description')
        new_goal.target_date = goals.validated_data.get('targetDate')

        new_goal.save(request_=self.request)

        response = GoalPostResponse({
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'goal': {
                'goalId': new_goal.pk,
                'goalName': new_goal.name,
                'description': new_goal.description,
                'targetDate': new_goal.target_date
            }
        }).data

        return response

    def __set_investment(self):
        investment = finance.models.Investment()

        investment.name = self.name
        investment.date = self.date
        investment.quantity = self.quantity
        investment.price = self.price
        investment.amount = self.amount
        investment.cash_flow = self.cash_flow
        investment.interest_rate = self.interest_rate
        investment.interest_index = self.interest_index
        investment.type_id = self.type_id
        investment.maturity_at = self.dat_maturity if self.dat_maturity not in ('', 'null') else None
        investment.custodian_id = self.custodian_id
        investment.index_id = '2a2b100f-17d9-4c61-b3b4-f06662113953'  # TODO: adjust to get from request
        investment.liquidity_id = '4f0a614b-3e11-46ab-817e-36f3a6de87f8'  # TODO: adjust to get from request
        investment.owner_id = self.owner_id
        investment.currency_id = 'BRL'  # TODO: adjust to get from request

        return investment
