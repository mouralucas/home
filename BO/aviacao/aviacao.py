import os
import sys
import time
from datetime import datetime
from os import listdir

import dateutil
import numpy as np
import pandas as pd
from django.db.models import F

import aviacao.models
import util.datetime


class Aviacaco:
    def __init__(self):
        pass

    def get_resumos(self):
        """
        :Nome da classe/função: get_resumos
        :descrição: Busca os resumos de voos, companhias/aeroportos com maior numero de voos
        :Criação: Lucas Penha de Moura - 03/09/2021
        :Edições:
            Motivo:
        :return:
        """
        pass

    def get_companhia_aerea(self):
        pass

    def import_csv(self, root_dir='/run/media/lucas/Dados/Aviacao/teste/',
                   uploaded_dir='/run/media/lucas/Dados/Aviacao/uploaded/'):
        """
        :Nome da classe/função: import_csv
        :descrição: Função para importar o csv buscado por aeroporto e companhia aerea
        :Criação: Lucas Penha de Moura
        :Edições:
        :return: None
        """
        if self._get_platform() == 'windows':
            root_dir = 'D:\\Aviacao\\teste\\'
            uploaded_dir = 'D:\\Aviacao\\uploaded\\'

        files = self._find_csv_filenames(path_to_dir=root_dir)
        airport_list = pd.DataFrame(list(aviacao.models.Aeroporto.objects.values('iata', 'id').exclude(iata__isnull=True)))

        for file in files:
            flights = pd.DataFrame([])

            for df in pd.read_csv(root_dir + file, iterator=True, chunksize=10000, skiprows=7):
                flights = flights.append(pd.DataFrame(df))

            merged = pd.merge(flights, airport_list, left_on='Destination Airport', right_on='iata', how='left')
            merged.drop(merged.tail(1).index, inplace=True)
            print('Aeroporto', len(airport_list.index))
            print('Voos', len(flights.index))
            print('Merged', len(merged.index))

            list_voo = []
            t1 = time.time()
            for index, row in merged.iterrows():
                voo = aviacao.models.Voo()

                # Delta = 2009
                # AA = 24
                # United = 5209

                # ATL = 3682
                # DFW = 3670
                # LAX = 3484
                # ORD = 3830

                voo.status = True
                voo.dat_insercao = datetime.now()
                voo.usr_insercao = 1
                voo.companhia_id = 2009
                voo.data = util.datetime.format_data_us(row['Date (MM/DD/YYYY)'])
                voo.nr_voo = row['Flight Number']
                voo.registro = row['Tail Number']
                voo.origem_id = 3682
                voo.destino_id = row['id']
                voo.partida_prevista = row['Scheduled departure time'] if row['Scheduled departure time'] != '24:00' else '00:00'
                voo.partida_real = row['Actual departure time'] if row['Actual departure time'] != '24:00' else '00:00'
                voo.tempo_corrido_previsto = row['Scheduled elapsed time (Minutes)']
                voo.tempo_corrido_real = row['Actual elapsed time (Minutes)']
                voo.partida_atraso = row['Departure delay (Minutes)']
                voo.weels_off = row['Wheels-off time'] if row['Wheels-off time'] != '24:00' else '00:00'
                voo.taxi_out = row['Taxi-Out time (Minutes)']
                voo.atraso_companhia = row['Delay Carrier (Minutes)']
                voo.atraso_tempo = row['Delay Weather (Minutes)']
                voo.atraso_nas = row['Delay National Aviation System (Minutes)']
                voo.atraso_seguranca = row['Delay Security (Minutes)']
                voo.atraso_aeronave = row['Delay Late Aircraft Arrival (Minutes)']
                voo.id = None
                list_voo.append(voo)

                print('Insert {0} de {1}: voo {2} no dia {3}'.format(index + 1, len(merged.index), voo.nr_voo, voo.data))

                if index != 0 and index % 10000 == 0:
                    aviacao.models.Voo.objects.bulk_create(list_voo)
                    list_voo = []
            t2 = time.time()

            aviacao.models.Voo.objects.bulk_create(list_voo)
            os.replace(root_dir + file, uploaded_dir + file)
            print('Finalizado o arquivo {0} no tempo de {1}'.format(file, t2 - t1))

        return {'status': True, 'descricao': ''}

    def import_csv_complemento(self, root_dir='/run/media/lucas/Dados/Projetos/Aviacao/upload/',
                               uploaded_dir='/run/media/lucas/Dados/Projetos/Aviacao/uploaded/'):
        """
        :Nome da classe/função: import_csv
        :descrição: Função para importar o csv com todas as companhias e separados por ano/mes
        :Criação: Lucas Penha de Moura - 07/09/2021
        :Edições:
        :return: None
        """

        # TODO: adicionar validação da data que está inserindo:
        # Primeiro nível: validar nome do arquivo com anomes do campo data
        # Segundo nível: mostar na tela e esperar confirmação do usuário
        # Tercro nivel: verificar hash das informaçoes no banco
        if self._get_platform() == 'windows':
            root_dir = 'D:\\Projetos\\Aviacao\\teste\\'
            uploaded_dir = 'D:\\Projetos\\Aviacao\\uploaded\\'

        files = self._find_csv_filenames(path_to_dir=root_dir)
        orig_airport_list = pd.DataFrame(list(aviacao.models.Aeroporto.objects.values('iata', 'id').annotate(id_origin=F('id'), iata_origin=F('iata'), tzoffset_origin=F('timezone_offset')).exclude(iata__isnull=True)))
        dest_airport_list = pd.DataFrame(list(aviacao.models.Aeroporto.objects.values('iata', 'id').annotate(id_dest=F('id'), iata_dest=F('iata'), tzoffset_dest=F('timezone_offset')).exclude(iata__isnull=True)))
        carrier_list = pd.DataFrame(list(aviacao.models.CompanhiaAerea.objects.values('iata', 'id').annotate(id_carrier=F('id'), iata_companhia=F('iata'))))

        for file in files:
            flights = pd.DataFrame([])

            # year = int(file[:4])
            # month = int(file[4:6])

            # recorded_flights = pd.DataFrame(list(aviacao.models.Voo.objects.filter(data__year=year, data__month=month)))

            # Faz a leitura do arquivo em blocos de 10 mil linhas e adiciona ao dateframe inicial

            dtype = {
                'FL_DATE': str,
                'OP_CARRIER_FL_NUM': str,
                'TAIL_NUM': str,
                'ORIGIN': str,
                'DEST': str,
                'CRS_DEP_TIME': str,
                'DEP_TIME': str,
                'DEP_DELAY': float,
                'WHEELS_OFF': str,
                'TAXI_OUT': float,
                'WHEELS_ON': str,
                'TAXI_IN': float,
                'CRS_ARR_TIME': str,
                'ARR_TIME': str,
                'ARR_DELAY': float,
                'CANCELLED': float,
                'DIVERTED': float,
                'CRS_ELAPSED_TIME': float,
                'ACTUAL_ELAPSED_TIME': float,
                'AIR_TIME': float,
                'DISTANCE': float,
                'CARRIER_DELAY': float,
                'WEATHER_DELAY': float,
                'NAS_DELAY': float,
                'SECURITY_DELAY': float,
                'LATE_AIRCRAFT_DELAY': float
            }
            for df in pd.read_csv(root_dir + file, iterator=True, chunksize=10000, encoding='latin-1', na_values=0, dtype=dtype):
                flights = flights.append(pd.DataFrame(df))

            pd.set_option('display.max_columns', None)

            # Realiza os joins para buscar o id dos aeroportos de origem e destino e o id da companhia aerea
            aux_1 = pd.merge(flights, orig_airport_list, left_on='ORIGIN', right_on='iata_origin', how='left')
            aux_2 = pd.merge(aux_1, dest_airport_list, left_on='DEST', right_on='iata_dest', how='left')
            csv_flights = pd.merge(aux_2, carrier_list, left_on='OP_CARRIER', right_on='iata_companhia', how='left')

            flight_list = []
            new_flights = csv_flights.replace({np.nan: None})
            for index, row in new_flights.iterrows():
                flight = aviacao.models.Voo()

                flight.dat_insercao = datetime.now()
                flight.usr_insercao = 1
                flight.companhia_id = row['id_carrier']
                flight.data = row['FL_DATE']
                flight.nr_voo = row['OP_CARRIER_FL_NUM']
                flight.registro = row['TAIL_NUM']

                flight.origem_id = row['id_origin']
                flight.destino_id = row['id_dest']

                flight.partida_tz_offset = row['tzoffset_origin']
                flight.chegada_tz_offset = row['tzoffset_dest']

                flight.partida_prevista = util.datetime.format_time(row['CRS_DEP_TIME']) if row['CRS_DEP_TIME'] != '2400' else '00:00'
                flight.dat_partida_prevista = util.datetime.concat_date_time(flight.data, flight.partida_prevista, tz_offset=flight.partida_tz_offset)
                flight.partida_real = util.datetime.format_time(row['DEP_TIME']) if row['DEP_TIME'] != '2400' else '00:00'
                flight.dat_partida_real = util.datetime.concat_date_time(flight.data, flight.partida_real, tz_offset=flight.partida_tz_offset)
                flight.partida_atraso = row['DEP_DELAY']
                flight.weels_off = util.datetime.format_time(row['WHEELS_OFF']) if row['WHEELS_OFF'] != '2400' else '00:00'
                flight.dat_weels_off = util.datetime.concat_date_time(flight.data, flight.weels_off, tz_offset=flight.partida_tz_offset)
                flight.taxi_out = row['TAXI_OUT']

                flight.weels_on = util.datetime.format_time(row['WHEELS_ON']) if row['WHEELS_ON'] != '2400' else '00:00'
                flight.dat_weels_on = util.datetime.concat_date_time(flight.data, flight.weels_on, tz_offset=flight.chegada_tz_offset)
                flight.taxi_in = row['TAXI_IN']
                flight.chegada_prevista = util.datetime.format_time(row['CRS_ARR_TIME']) if row['CRS_ARR_TIME'] != '2400' else '00:00'
                flight.dat_chegada_prevista = util.datetime.concat_date_time(flight.data, flight.chegada_prevista, tz_offset=flight.chegada_tz_offset)
                flight.chegada_real = util.datetime.format_time(row['ARR_TIME']) if row['ARR_TIME'] != '2400' else '00:00'
                flight.dat_chegada_real = util.datetime.concat_date_time(flight.data, flight.chegada_real, tz_offset=flight.chegada_tz_offset)
                flight.chegada_atraso = row['ARR_DELAY']
                flight.is_cancelado = row['CANCELLED'] = True if row['CANCELLED'] == 1 else False
                flight.is_alternado = row['DIVERTED'] = True if row['DIVERTED'] == 1 else False
                flight.tempo_corrido_previsto = row['CRS_ELAPSED_TIME']
                flight.tempo_corrido_real = row['ACTUAL_ELAPSED_TIME']
                flight.tempo_ar = row['AIR_TIME']
                flight.distancia = row['DISTANCE']
                flight.atraso_companhia = row['CARRIER_DELAY']
                flight.atraso_tempo = row['WEATHER_DELAY']
                flight.atraso_nas = row['NAS_DELAY']
                flight.atraso_seguranca = row['SECURITY_DELAY']
                flight.atraso_aeronave = row['LATE_AIRCRAFT_DELAY']

                flight.id = None

                flight_list.append(flight)

                print('Insert {0} de {1}: voo no dia {2}'.format(index + 1, len(new_flights.index), flight.data))

                if index != 0 and index % 15000 == 0:
                    aviacao.models.Voo.objects.bulk_create(flight_list)
                    # print(flight_list)
                    flight_list = []

            aviacao.models.Voo.objects.bulk_create(flight_list)
            os.replace(root_dir + file, uploaded_dir + file)
            print('Finalizado o arquivo {0}'.format(file))

    def count_row_csv(self, root_dir='/run/media/lucas/Dados/Projetos/Aviacao/teste/'):

        if self._get_platform() == 'windows':
            root_dir = 'D:\\Aviacao\\teste\\'

        files = self._find_csv_filenames(path_to_dir=root_dir)
        orig_airport_list = pd.DataFrame(list(aviacao.models.Aeroporto.objects.values('iata', 'id').annotate(id_origin=F('id'), iata_origin=F('iata'), tzoffset_origin=F('timezone_offset')).exclude(iata__isnull=True)))
        dest_airport_list = pd.DataFrame(list(aviacao.models.Aeroporto.objects.values('iata', 'id').annotate(id_dest=F('id'), iata_dest=F('iata'), tzoffset_dest=F('timezone_offset')).exclude(iata__isnull=True)))
        carrier_list = pd.DataFrame(list(aviacao.models.CompanhiaAerea.objects.values('iata', 'id').annotate(id_carrier=F('id'), iata_companhia=F('iata'))))

        flights = pd.DataFrame([])
        for file in files:
            dtype = {
                'FL_DATE': str,
                'OP_CARRIER_FL_NUM': str,
                'TAIL_NUM': str,
                'ORIGIN': str,
                'DEST': str,
                'CRS_DEP_TIME': str,
                'DEP_TIME': str,
                'DEP_DELAY': float,
                'WHEELS_OFF': str,
                'TAXI_OUT': float,
                'WHEELS_ON': str,
                'TAXI_IN': float,
                'CRS_ARR_TIME': str,
                'ARR_TIME': str,
                'ARR_DELAY': float,
                'CANCELLED': float,
                'DIVERTED': float,
                'CRS_ELAPSED_TIME': float,
                'ACTUAL_ELAPSED_TIME': float,
                'AIR_TIME': float,
                'DISTANCE': float,
                'CARRIER_DELAY': float,
                'WEATHER_DELAY': float,
                'NAS_DELAY': float,
                'SECURITY_DELAY': float,
                'LATE_AIRCRAFT_DELAY': float
            }
            for df in pd.read_csv(root_dir + file, iterator=True, chunksize=10000, encoding='latin-1', na_values=0, dtype=dtype):
                flights = flights.append(pd.DataFrame(df))


        pd.set_option('display.max_columns', None)

        # Realiza os joins para buscar o id dos aeroportos de origem e destino e o id da companhia aerea
        aux_1 = pd.merge(flights, orig_airport_list, left_on='ORIGIN', right_on='iata_origin', how='left')
        aux_2 = pd.merge(aux_1, dest_airport_list, left_on='DEST', right_on='iata_dest', how='left')
        csv_flights = pd.merge(aux_2, carrier_list, left_on='OP_CARRIER', right_on='iata_companhia', how='left')

        flight_list = []
        new_flights = csv_flights.replace({np.nan: None})

        return {'status': True, 'tamanho': len(new_flights.index)}

    def set_datetime(self):
        flights = aviacao.models.Voo.objects.filter(data__range=('2001-09-11', '2001-09-11'))

        for i in flights:
            data = i.data
            tzo = i.origem.timezone_offset
            tzd = i.destino.timezone_offset

            hr_partida_prevista = i.partida_prevista
            hr_partida_real = i.partida_real
            hr_chegada_prevista = i.chegada_prevista
            hr_chegada_real = i.chegada_real

            # updated_flights = i.dat_partida_prevista = dateutil.parser.parse('2013-09-11 00:17 -5')
            updated_flights = i.dat_partida_prevista = dateutil.parser.parse(data + ' ' + hr_partida_prevista + ' ' + tzo)


    def clean_duplicates(self, fields=None):
        ano_filtro = 2015

        for i in range(1988, 1989):
            print('Gerando duplicados de {}'.format(i))

            voos = aviacao.models.Voo.objects.filter(data__year=i)

            df = pd.DataFrame(list(voos.values('id',
                                               'data',
                                               'nr_voo',
                                               'registro',
                                               'partida_prevista',
                                               'partida_real',
                                               'tempo_corrido_previsto',
                                               'tempo_corrido_real',
                                               'partida_atraso',
                                               'taxi_out',
                                               'atraso_companhia',
                                               'atraso_tempo',
                                               'atraso_nas',
                                               'atraso_seguranca',
                                               'atraso_aeronave',
                                               'destino_id',
                                               'companhia__iata',
                                               'origem__iata'
                                               )))

            duplicates = df[df.duplicated(['data',
                                           'nr_voo',
                                           'registro',
                                           'partida_prevista',
                                           'partida_real',
                                           'tempo_corrido_previsto',
                                           'tempo_corrido_real',
                                           'partida_atraso',
                                           'taxi_out',
                                           'atraso_companhia',
                                           'atraso_tempo',
                                           'atraso_nas',
                                           'atraso_seguranca',
                                           'atraso_aeronave',
                                           'destino_id'])]

            duplicates.to_csv('/run/media/lucas/Dados/Projetos/Aviacao/teste/duplicados_{}.csv'.format(str(i)))

        return {'status': True, 'duplicados': None}

    def _find_csv_filenames(self, path_to_dir, suffix=".csv"):
        filenames = listdir(path_to_dir)
        return [filename for filename in filenames if filename.endswith(suffix)]

    def _get_platform(self):
        platforms = {
            'linux1': 'linux',
            'linux2': 'linux',
            'darwin': 'osx',
            'win32': 'windows'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]
