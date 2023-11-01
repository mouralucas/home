
import pandas as pd

import util.datetime


class File:
    def __init__(self):
        pass

    def upload(self):
        pass

    def extract_table_pdf(self, path, pdf_origin='picpay_statement'):
        # reads table from pdf file
        if pdf_origin == 'picpay_statement':
            self.__picpay_statement(path=path)
        elif pdf_origin == 'nubank_bill':
            pass

    def __picpay_statement_beta(self, dataframe):
        """
        :Name: __picpay_statement
        :Description: Handles information about PicPay statement format
        :Created by: Lucas Penha de Moura - 25/09/2022
        :Edited by:

        Explicit params:
        :param dataframe: the dataframe with the data read from input pdf

        Implicit params (passed in the class instance or set by other functions):
        None
        """
        output_path = 'media/finance/statement/'
        output_name = 'a.csv'

        new_columns = {
            'Data/Hora': 'date',
            'Unnamed: 0': 'description',
            'Descrição das Movimentações': 'amount',
        }

        dataframe = pd.concat(dataframe)
        dataframe = dataframe.rename(columns=new_columns)
        dataframe = dataframe[dataframe.columns[dataframe.columns.isin(list(new_columns.values()))]]

        dataframe['date'] = dataframe['date'].apply(lambda x: x.replace('\r', ' '))
        dataframe['amount'] = dataframe['amount'].apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', ''))

        dataframe['amount'] = dataframe['amount'].apply(lambda x: float(x))

        dataframe['reference'] = dataframe['date'].apply(lambda x: util.datetime.DateTime.get_period(x.split(' ')[0], input_format='%d/%M/y'))
        dataframe.reset_index(inplace=True)

        agg = dataframe.groupby(['reference'])
        for group in agg:
            group[1].to_csv(output_path + 'picpay_statement_' + str(group[0]) + '.csv')

        return dataframe

    def __nubank_bill(self, dataframe):
        pass

    # def __picpay_statement(self, path):
    #     # Melhor implementação com Camelot
    #
    #     new_columns = {
    #         'Data/Hora': 'date',
    #         'Descrição das Movimentações': 'description',
    #         'Valor': 'amount',
    #     }
    #
    #     tables = camelot.read_pdf(path, pages='1-end')
    #     df = pd.concat([table.df.rename(columns=table.df.iloc[0]).drop(table.df.index[0]) for table in tables])
    #     df = df.rename(columns=new_columns)
    #
    #     # Remove unnecessary columns
    #     df = df[df.columns[df.columns.isin(list(new_columns.values()))]]
    #
    #     # Clean data
    #     df['date'] = df['date'].apply(lambda x: x.replace('\r', ' ').replace('\n', ' '))
    #     df['amount'] = df['amount'].apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', ''))
    #     df['amount'] = df['amount'].apply(lambda x: float(x))
    #     df['period'] = df['date'].apply(lambda x: util.datetime.DateTime.get_period(x.split(' ')[0], is_date_str=True, input_format='%d/%m/%Y'))
    #
    #     # df['cumulated'] = df['amount'].cumsum()
    #
    #     list_period = df.groupby("period")
    #     for i in list_period:
    #         aux = i[1]
    #         aux['cumulated'] = aux['amount'].cumsum()
    #         print(aux)
    #
    #
    #     # df['acumulado'] = df.groupby(['date']).cumsum()
    #
    #     # df.to_excel('teste.xlsx', index=False)
    #     print('')

