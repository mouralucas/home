from os import listdir

import pandas as pd
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView

import BO.aviacao.aviacao


class Home(View):
    def get(self, *args, **kwargs):
        pass


class ImportVooCsv(APIView):
    def get(self, *args, **kwargs):
        response = BO.aviacao.aviacao.Aviacaco().import_csv_complemento()

        return JsonResponse(response, safe=False)


class TamanhoCSV(View):
    def get(self, *args, **kwargs):
        response = BO.aviacao.aviacao.Aviacaco().clean_duplicates()

        return JsonResponse(response, safe=False)


class Geral(APIView):
    def get(self, *args, **kwargs):
        # response = BO.aviacao.aviacao.Aviacaco().count_row_csv()
        # response = BO.aviacao.aviacao.Aviacaco().clean_duplicates()
        response = BO.aviacao.aviacao.Aviacaco().set_datetime()

        return JsonResponse(response, safe=False)


class ImportAeroportoCsv(APIView):
    def get(self, *args, **kwargs):
        root_dir = '/home/lucas/Documents/Aviacao/Aux/' + kwargs.get('file') + '.csv'

        flights = pd.DataFrame([])

        for df in pd.read_csv(root_dir, iterator=True, chunksize=10000, skiprows=7):
            flights = flights.append(pd.DataFrame(df))

        # TODO: adicionar regras para verificar se o registro existe e atualziar com os códigos IATA e ICAO
        for index, row in flights.iterrows():
            pass


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]
