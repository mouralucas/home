import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


def open_excel(path=None):
    df = pd.read_excel(path, sheet_name='Livros')

    print("Column headings:")
    print(df.columns)
    print(df['ISBN'])

    for i in df['ISBN']:
        print(i.replace('-', ''))

