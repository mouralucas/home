import pathlib
import pandas as pd


class Files:
    def __init__(self, file):
        self.file = file
        self.allowed_extensions = ['.txt', '.csv', '.xml', '.yaml', '.xlsx']

        self.__validate_file_extension()

    def open_csv(self):
        """
        Open a csv file and import into a DataFrame and return
        """
        pass

    def open_excel(self, sheet_name):
        """
        Open an Excel file and import into a DataFrame and return
        """
        df = pd.read_excel(self.file, sheet_name=sheet_name)
        print(df)

    def open_xml(self, separator=','):
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
