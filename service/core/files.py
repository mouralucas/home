import pathlib
import pandas as pd


class Files:
    """
    :Name: CustomSerializer
    :Created by: Lucas Penha de Moura - 04/01/2024
    :Edited by:

    This service is used when a file need to be validated before used.
    """

    def __init__(self, file):
        self.file = file
        self.allowed_extensions = ['.txt', '.csv', '.xml', '.yaml', '.xlsx']

        self.__validate_file_extension()
        # TODO: after validate ext, call the function that opens the file, maybe use a param that asks
        # if the user want the return automatically, something like 'return_df'

    def open_csv(self, separator=',', encoding='utf-8', index_col=None):
        """
        Open a csv file and import into a DataFrame and return
        It only apply the specified values in parameters
        """
        df = pd.read_csv(self.file, sep=separator, encoding=encoding, index_col=index_col)
        return df

    def open_excel(self, sheet_name):
        """
        Open an Excel file and import into a DataFrame and return
        """
        df = pd.read_excel(self.file, sheet_name=sheet_name)
        print(df)

    def open_xml(self):
        """
        Open a xml file and import into a DataFrame and return
        """
        pass

    def open_yaml(self, file_path):
        """
        Open a yaml file and import into a DataFrame and return
        """
        pass

    def __validate_file_extension(self):
        """
        Raise exception if not in file extensions list
        """
        ext = pathlib.Path(self.file).suffix
        if ext not in self.allowed_extensions:
            raise Exception("")
