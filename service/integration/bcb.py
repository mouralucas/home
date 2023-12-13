import pandas as pd

import finance.models
from service.integration.integration import Integration

DAILY_PERIODICITY = 'b9f83ad5-7701-4098-bdaf-ee092f3247eb'
MONTHLY_PERIODICITY = 'dc5b3bf8-2b84-423a-9a90-e7e194e355fa'
YEARLY_PERIODICITY = '9f4980b8-9c8f-4cce-90e2-af3c03867059'


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
    433     Índice nacional de preços ao consumidor-amplo (IPCA)
    1178    Taxa de juros - Selic anualizada base 252

    4389	Taxa de juros - CDI anualizada base 252
    4391    Taxa de juros - CDI acumulada no mês

    Integration with the Banco Central do Brasil open data API
    """

    def __init__(self, service=None):
        super().__init__(service)
        self.url_bcdata = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{0}/dados?{1}'

    def historical_data_cdi(self):
        ########################## CDI Daily ##########################
        cdi_interest_daily = pd.read_json(self.url_bcdata.format('12', ''))
        cdi_interest_daily['data'] = pd.to_datetime(cdi_interest_daily['data'], dayfirst=True)

        historical_cdi_daily_data = finance.models.FinanceData.objects.filter(index_id='2a2b100f-17d9-4c61-b3b4-f06662113953',
                                                                              periodicity=DAILY_PERIODICITY)
        historical_cdi_daily_data.delete()
        list_cdi_historical = []
        for idx, item in cdi_interest_daily.iterrows():
            aux = finance.models.FinanceData(
                name='CDI',
                index_id='2a2b100f-17d9-4c61-b3b4-f06662113953',
                date=item['data'],
                reference=self.__set_reference(item['data']),
                value=item['valor'],
                periodicity_id='b9f83ad5-7701-4098-bdaf-ee092f3247eb',
                unit='% a.d.'
            )
            list_cdi_historical.append(aux)
        finance.models.FinanceData.objects.bulk_create(list_cdi_historical)

        ########################## CDI Monthly ##########################
        cdi_interest_monthly = pd.read_json(self.url_bcdata.format('4391', ''))
        cdi_interest_monthly['data'] = pd.to_datetime(cdi_interest_monthly['data'], dayfirst=True)

        historical_cdi_monthly_data = finance.models.FinanceData.objects.filter(index_id='2a2b100f-17d9-4c61-b3b4-f06662113953',
                                                                                periodicity=MONTHLY_PERIODICITY)
        historical_cdi_monthly_data.delete()
        list_cdi_historical_monthly = []
        for idx, item in cdi_interest_monthly.iterrows():
            aux = finance.models.FinanceData(
                name='CDI',
                index_id='2a2b100f-17d9-4c61-b3b4-f06662113953',
                date=item['data'],
                reference=self.__set_reference(item['data']),
                value=item['valor'],
                periodicity_id='dc5b3bf8-2b84-423a-9a90-e7e194e355fa',
                unit='% a.m.'
            )
            list_cdi_historical_monthly.append(aux)
        finance.models.FinanceData.objects.bulk_create(list_cdi_historical_monthly)

        # Monthly data

        # Yearly data

        for idx, value in cdi_interest_daily.iterrows():
            print(value)

        print(cdi_interest_daily)

    def historical_data_selic(self):
        selic_interest_daily = pd.read_json(self.url_bcdata.format('11', ''))
        selic_interest_daily['data'] = pd.to_datetime(selic_interest_daily['data'], dayfirst=True)

        historical_selic_daily_data = finance.models.FinanceData.objects.filter(index_id='b7e5c4a0-3b65-4b1f-86d8-3797ef1a91a0',
                                                                                periodicity=DAILY_PERIODICITY)
        historical_selic_daily_data.delete()

        list_selic_historical = []
        for idx, item in selic_interest_daily.iterrows():
            aux = finance.models.FinanceData(
                name='SELIC',
                index_id='b7e5c4a0-3b65-4b1f-86d8-3797ef1a91a0',
                date=item['data'],
                reference=self.__set_reference(item['data']),
                value=item['valor'],
                periodicity_id='b9f83ad5-7701-4098-bdaf-ee092f3247eb',
                unit='% a.d.'
            )
            list_selic_historical.append(aux)
        finance.models.FinanceData.objects.bulk_create(list_selic_historical)

    def historical_data_ipca(self):
        ipca_am = pd.read_json(self.url_bcdata.format('433', ''))
        ipca_am['data'] = pd.to_datetime(ipca_am['data'], dayfirst=True)

        historical_ipca_monthly_data = finance.models.FinanceData.objects.filter(index_id='ef07cbb0-9b29-43c6-a060-bef73f1cc000',
                                                                                 periodicity_id=MONTHLY_PERIODICITY)
        historical_ipca_monthly_data.delete()

        list_ipca_historical = []
        for idx, item in ipca_am.iterrows():
            aux = finance.models.FinanceData(
                name='IPCA',
                index_id='ef07cbb0-9b29-43c6-a060-bef73f1cc000',
                date=item['data'],
                reference=self.__set_reference(item['data']),
                value=item['valor'],
                periodicity_id='dc5b3bf8-2b84-423a-9a90-e7e194e355fa',
                unit='% a.m.'
            )
            list_ipca_historical.append(aux)
        ipca_monthly = finance.models.FinanceData.objects.bulk_create(list_ipca_historical)

        response = {
            'ipca_monthly_qtd': len(ipca_monthly)
        }

        return

    def __set_reference(self, date):
        year = date.year
        month = date.month
        return year * 100 + month
