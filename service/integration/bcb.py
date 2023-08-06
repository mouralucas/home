import finance.models
from service.integration.integration import Integration
import pandas as pd


class BancoCentralAPI(Integration):
    """
    :Name: format_data
    :Description: Format the date into the requestd format
    :Created by: Lucas Penha de Moura - 03/04/2020
    :Edited by:

    Fetch and persist data from SGS into database
    Data codes:
    11	    Taxa de juros - Selic
    432     Taxa de juros - Meta Selic definida pelo Copom
    1178    Taxa de juros - Selic anualizada base 252
    4389	Taxa de juros - CDI anualizada base 252

    Integration with the Banco Central do Brasil open data API
    """
    def __init__(self, service=None):
        super().__init__(service)
        self.url_bcdata = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{0}/dados?{1}'

    def historical_data_selic_integration(self):
        cdi_interest = pd.read_json(self.url_bcdata.format('12', 'dataInicial=01/08/2023&dataFinal=31/08/2023'))
        cdi_interest['data'] = pd.to_datetime(cdi_interest['data'], dayfirst=True)

        historical_data = finance.models.FinanceData.objects.filter(name='cdi', periodicity='% a.d.')

        for idx, value in cdi_interest.iterrows():
            print(value)

        print(cdi_interest)

    def daily_selic_update(self):
        pass