## TODO: create const to save columns for all available pos and user it to call file service and return cleaned df
from decimal import Decimal

import numpy as np
import pandas as pd

from finance.models import PosStatement
from service.core.files import Files
from django.utils import timezone

from service.finance.finance import Finance


class PointOfSales(Finance):
    def __init__(self):
        super().__init__()
        self.pagseguro_columns = {
            'Transacao_ID': 'transaction_id',
            'Debito_Credito': 'cash_flow_id',
            'Status': 'transaction_status',
            'Tipo_Pagamento': 'method',
            'Valor_Bruto': 'amount_gross',
            'Valor_Desconto': 'amount_discount',
            'Valor_Taxa': 'amount_fee',
            'Valor_Liquido': 'amount_net',
            'Data_Transacao': 'transaction_date',
            'Data_Compensacao': 'settlement_date',
            'Bandeira_Cartao_Credito': 'credit_card_brand'
        }
        # TODO: create functions here that delegate to correct provider function or that cleans every provider for a common df

    def import_statement(self, file):
        statement_df = Files(file=file).open_csv(separator=';', encoding='latin1', index_col=False)
        statement_df = statement_df[self.pagseguro_columns.keys()]
        statement_df = statement_df.rename(columns=self.pagseguro_columns)

        # TODO: create generic function to handle this cleaning
        statement_df['cash_flow_id'] = statement_df['cash_flow_id'].apply(lambda x: 'INCOMING' if x == 'Crédito' else 'OUTGOING')
        statement_df['amount_gross'] = statement_df['amount_gross'].str.replace('.', '')
        statement_df['amount_gross'] = statement_df['amount_gross'].str.replace(',', '.').apply(lambda x: Decimal(x))
        statement_df['amount_discount'] = statement_df['amount_discount'].str.replace(',', '.').apply(lambda x: Decimal(x))
        statement_df['amount_fee'] = statement_df['amount_fee'].str.replace(',', '.').apply(lambda x: Decimal(x))
        statement_df['amount_net'] = statement_df['amount_net'].str.replace('.', '')
        statement_df['amount_net'] = statement_df['amount_net'].str.replace(',', '.').apply(lambda x: Decimal(x))
        statement_df['transaction_date'] = pd.to_datetime(statement_df['transaction_date'], dayfirst=True)
        statement_df['settlement_date'] = pd.to_datetime(statement_df['settlement_date'], dayfirst=True)

        statement_df = statement_df.fillna(np.nan).replace([np.nan], [None])

        list_pos_statement_entry = []
        for idx, row in statement_df.iterrows():
            statement_entry = PosStatement(
                created_at=timezone.now(),
                transaction_id=row['transaction_id'],
                cash_flow_id=row['cash_flow_id'],
                transaction_status=row['transaction_status'],
                method=row['method'],
                amount_gross=(row['amount_gross']),
                amount_discount=(row['amount_discount']),
                amount_fee=row['amount_fee'],
                amount_net=row['amount_net'],
                transaction_date=row['transaction_date'],
                settlement_date=row['settlement_date'],
                credit_card_brand=row['credit_card_brand']
            )
            list_pos_statement_entry.append(statement_entry)

        PosStatement.objects.bulk_create(list_pos_statement_entry)

        print(statement_df)

    def get_providers(self):
        pass
