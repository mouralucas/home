import finance.models
from service.integration.integration import Integration
import pandas as pd
from datetime import datetime, timedelta

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

    def historical_data_cdi(self):
        start_date = datetime(2023, 8, 1)
        end_date = datetime(2023, 8, 31)

        # Daily data
        cdi_interest_ad = pd.read_json(self.url_bcdata.format('12', ''))
        cdi_interest_ad['data'] = pd.to_datetime(cdi_interest_ad['data'], dayfirst=True)

        historical_cdi_ad_data = finance.models.FinanceData.objects.filter(name='CDI', periodicity='b9f83ad5-7701-4098-bdaf-ee092f3247eb')
        historical_cdi_ad_data.delete()
        list_cdi_historical = []
        for idx, item in cdi_interest_ad.iterrows():
            aux = finance.models.FinanceData(
                name='CDI',
                date=item['data'],
                value=item['valor'],
                periodicity_id='b9f83ad5-7701-4098-bdaf-ee092f3247eb',
                unit='% a.d.'
            )
            list_cdi_historical.append(aux)
        finance.models.FinanceData.objects.bulk_create(list_cdi_historical)

        # Interest rate - CDI in annual terms (basis 252)
        # cdi_interest_annual_ad = pd.read_json(self.url_bcdata.format('4389', ''))
        # cdi_interest_annual_ad['data'] = pd.to_datetime(cdi_interest_ad['data'], dayfirst=True)
        #
        # historical_cdi_ad_data = finance.models.FinanceData.objects.filter(name='CDI', periodicity='b9f83ad5-7701-4098-bdaf-ee092f3247eb')
        # historical_cdi_ad_data.delete()
        # list_cdi_historical = []
        # for idx, item in cdi_interest_ad.iterrows():
        #     aux = finance.models.FinanceData(
        #         name='CDI',
        #         date=item['data'],
        #         value=item['valor'],
        #         periodicity_id='b9f83ad5-7701-4098-bdaf-ee092f3247eb',
        #         unit='% a.d.'
        #     )
        #     list_cdi_historical.append(aux)
        # finance.models.FinanceData.objects.bulk_create(list_cdi_historical)

        # Monthly data

        # Yearly data



        for idx, value in cdi_interest_ad.iterrows():
            print(value)

        print(cdi_interest_ad)

    def historical_data_selic(self):
        selic_interest_ad = pd.read_json(self.url_bcdata.format('11', 'dataInicial=01/08/2023&dataFinal=31/08/2023'))
        selic_interest_ad['data'] = pd.to_datetime(selic_interest_ad['data'], dayfirst=True)

        historical_selic_ad_data = finance.models.FinanceData.objects.filter(name='SELIC', periodicity='% a.d.')

        for idx, value in selic_interest_ad.iterrows():
            print(value)

        print(selic_interest_ad)
