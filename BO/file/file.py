from tabula import read_pdf, convert_into
import pandas as pd

import finance.models
import util.datetime


class File:
    def __init__(self):
        pass

    def upload(self):
        pass

    def extract_table_pdf(self, path, pdf_origin='picpay_statement'):
        # reads table from pdf file
        df = read_pdf(path, pages="all")

        if pdf_origin == 'picpay_statement':
            self.__picpay_statement(df)
        elif pdf_origin == 'nubank_bill':
            pass

    def __picpay_statement(self, dataframe):
        """
        :Name: __picpay_statement
        :Description: Handles information aboute PicPay statement format
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

        dataframe['reference'] = dataframe['date'].apply(lambda x: self.__set_reference(x.split(' ')[0]))
        dataframe.reset_index(inplace=True)

        agg = dataframe.groupby(['reference'])
        for group in agg:
            group[1].to_csv(output_path + 'picpay_statement_' + str(group[0]) + '.csv')

        return dataframe

    def __nubank_bill(self, dataframe):
        pass

    def __set_reference(self, date):
        dat_compra_date = util.datetime.data_to_datetime(date, formato='%d/%m/%Y')
        referencia_ano = dat_compra_date.year
        referencia_mes = dat_compra_date.month
        return referencia_ano * 100 + referencia_mes
