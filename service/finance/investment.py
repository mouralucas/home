import decimal
import json
import warnings

import pandas as pd
from django.db.models import F, Sum

import finance.models
from service.finance.finance import Finance


class Investment(Finance):
    def __init__(self, investment_id=None, parent_id=None, name=None, date=None, quantity=None, price=None, amount=None, cash_flow=None, interest_rate=None, interest_index=None, investment_type_id=None, dat_maturity=None, custodian_id=None,
                 owner_id=None, reference=None, request=None):
        super().__init__(reference=reference, amount=amount)

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
        self.request = request

    def set_investment(self):

        self.amount = decimal.Decimal(self.amount) * -1 if self.cash_flow == 'OUTGOING' else self.amount

        if not self.parent_id:
            # The first entry of the investment contains 2 rows, the first (without parent_id) is the total of the investment
            #   Any other row (with parent_id) representes each transaction in the investment, and changes the amount of the parent
            investment = self.__set_investment()
            investment.save(request_=self.request)

            child_investment = finance.models.Investment.objects.filter(pk=investment.pk).first()
            child_investment.pk = None
            child_investment.parent_id = investment.pk
            child_investment.save(request_=self.request)

        else:
            parent_investment = finance.models.Investment.objects.filter(pk=self.parent_id).first()
            parent_investment.amount += decimal.Decimal(self.amount)
            parent_investment.interest_index = 'Variable' if self.interest_index.strip() != parent_investment.interest_index else parent_investment.interest_index
            parent_investment.save(request_=self.request)

            child_investment = self.__set_investment()
            child_investment.save(request_=self.request)

        response = {
            'success': True,
        }
        return response

    def get_investment(self, show_mode):
        filters = {}

        if show_mode != 'all':
            filters['parent_id__isnull'] = True if show_mode == 'father' else False

        if self.investment_id:
            filters['pk'] = self.investment_id

        investments = finance.models.Investment.objects.values('name', 'description', 'amount', 'price', 'quantity',
                                                               'date') \
            .annotate(investmentId=F('pk'),
                      maturityDate=F('dat_maturity'),
                      interestRate=F('interest_rate'),
                      interestIndex=F('interest_index'),
                      custodianName=F('custodian__name'),
                      custodianId=F('custodian_id'),
                      investmentTypeId=F('type_id'),
                      investmentTypeName=F('type__name'),
                      parentId=F('parent_id')).order_by('-date').active().filter(**filters)

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

        investment_type = finance.models.InvestmentType.objects.values('id', 'name', 'description').filter(**filters).order_by('name')

        response = {
            'success': True,
            'description': None,
            'investmentType': list(investment_type)
        }

        return response

    def get_proportion(self):
        proportion = finance.models.Investment.objects.values('type__name').annotate(total=Sum('amount'))

        response = {
            'success': True,
            'investmentProportion': list(proportion)
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
        investment.dat_maturity = self.dat_maturity if self.dat_maturity not in ('', 'null') else None
        investment.custodian_id = self.custodian_id
        investment.parent_id = self.parent_id
        investment.owner_id = self.owner_id

        return investment
