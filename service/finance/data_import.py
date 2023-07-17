import pandas as pd


class Pagbank:
    def __init__(self, path=None):
        self.path = path

    def excel(self):
        statement = pd.read_excel(self.path, sheet_name='Sheet0', skiprows=8, na_filter=False)

        print('')
