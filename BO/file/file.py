from tabula import read_pdf, convert_into
import pandas as pd


class File:
    def __init__(self):
        pass

    def upload(self):
        pass

    def extract_table_pdf(self, path):
        # reads table from pdf file
        # df = read_pdf('picpay.pdf', pages="all")
        # dfs = pd.concat(df, axis=1)

        columns = ['Data/Hora', 'Descrição das Movimentações', 'Valor', 'Saldo', 'Saldo Sacável ']

        df = pd.read_csv('D:/System/Documents/mega/Financeiro/2022/PicPay2022.01.csv', encoding='latin1', delimiter=';')
        df = df[df.columns[df.columns.isin(columns)]]

        df['Valor'] = df['Valor'].apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', ''))
        df['Saldo'] = df['Saldo'].apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', ''))
        df['Saldo Sacável '] = df['Saldo Sacável '].apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', ''))

        df['Valor'] = df['Valor'].apply(lambda x: float(x))
        df['Saldo'] = df['Saldo'].apply(lambda x: float(x))
        df['Saldo Sacável '] = df['Saldo Sacável '].apply(lambda x: float(x.replace('-', '0')))

        df.to_csv('output_2.csv', encoding='latin1')

        print('')

        convert_into('picpay.pdf', "output.csv", output_format="csv", pages='all')

