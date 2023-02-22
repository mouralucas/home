import warnings
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def format_data(date, mask='____-__-__'):
    """
    :Name: format_data
    :Description: Format the date into the requestd format
    :Created by: Lucas Penha de Moura - 03/04/2020
    :Edited by:

    Explicit params:
    :param date: A data a ser convertida
    :param mask: Formato de saída da data

    Implicit params (passed in the class instance or set by other functions):
    None
    
    :return Data formatada de acordo com a mascara
    """
    warnings.warn('Função depreciada devido a criação de classe DateTime.', DeprecationWarning, stacklevel=2)
    data_formatada = date

    if date is None or date == '':
        return None

    if mask == '____-__-__':
        cleaned_data = str(date).replace("/", "")

        ano = cleaned_data[4:8]
        mes = cleaned_data[2:4]
        dia = cleaned_data[:2]

        data_formatada = str(ano) + '-' + str(mes) + '-' + str(dia)
    elif mask == '__/__/____':
        cleaned_data = str(date).replace("-", "")

        ano = cleaned_data[:4]
        mes = cleaned_data[4:6]
        dia = cleaned_data[6:8]

        data_formatada = str(dia) + '/' + str(mes) + '/' + str(ano)

    return data_formatada


def format_data_us(data, mask='____-__-__'):
    """
    Autor: Lucas Penha de Moura - 03 de abril de 2020

    Função para formatação de data de acordo com a necessidade
    Formatos suportados:
        -> Entrada: dd/mm/aaaa - Saída: aaaa-mm-dd (mask=____-__-__) - DEFAULT
        -> Entrada: aaaa-mm-dd - Saída: dd/mm/aaaa (mask=__/__/____)

    :param data: A data a ser convertida
    :param mask: Formato de saída da data
    :return: Data formatada de acordo com a mascara
    """
    warnings.warn('Função depreciada devido a criação de classe DateTime.', DeprecationWarning, stacklevel=2)
    if data is None or data == '':
        return None

    if mask == '____-__-__':
        cleaned_data = str(data).replace("/", "")

        ano = cleaned_data[4:8]
        dia = cleaned_data[2:4]
        mes = cleaned_data[:2]

        data_formatada = str(ano) + '-' + str(mes) + '-' + str(dia)
    elif mask == '__/__/____':
        cleaned_data = str(data).replace("-", "")

        ano = cleaned_data[:4]
        dia = cleaned_data[4:6]
        mes = cleaned_data[6:8]

        data_formatada = str(dia) + '/' + str(mes) + '/' + str(ano)

    return data_formatada


def format_time(str_time):
    warnings.warn('Função depreciada devido a criação de classe DateTime.', DeprecationWarning, stacklevel=2)
    try:
        str_time = str_time.zfill(4)
        str_time = str_time[:2] + ':' + str_time[2:]
    except Exception as e:
        str_time = None

    return str_time


# def historico_anomes():
#     mes_inicio = 1
#     ano_inicio = 2018
#
#     end_date = timezone.localdate() + relativedelta(months=6)
#
#     mes_fim = end_date.month
#     ano_fim = end_date.year
#
#     qtd_meses = (ano_fim - ano_inicio) * 12 + mes_fim - mes_inicio
#
#     meses = []
#     for i in range(0, qtd_meses + 1):
#         aux = {
#             'value': ano_inicio * 100 + mes_inicio,
#             'text': monthname(mes_inicio) + ' ' + str(ano_inicio),
#             'is_autual': None
#         }
#         meses.append(aux)
#
#         mes_inicio += 1
#         if mes_inicio > 12:
#             mes_inicio = 1
#             ano_inicio += 1
#
#     return meses


def monthname(month):
    warnings.warn('Função depreciada devido a criação de classe DateTime.', DeprecationWarning, stacklevel=2)
    monthname_pt = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
                    "Setembro", "Outubro", "Novembro", "Dezembro")


def split_anomes(anomes=None):
    warnings.warn('Função depreciada devido a criação de classe DateTime.', DeprecationWarning, stacklevel=2)
    try:
        mes = anomes[4:]
        ano = anomes[:4]
    except Exception as e:
        print(e)

        mes_atual = timezone.localdate().month
        ano_atual = timezone.localdate().year
        anomes = ano_atual * 100 + mes_atual
        mes = anomes[4:]
        ano = anomes[:4]

    response = {
        'ano': ano,
        'mes': mes
    }

    return response


def date_to_datetime(date_str, output_format='%Y-%m-%d'):
    try:
        return datetime.strptime(date_str, output_format)
    except Exception as e:
        print(e)
        return None


def concat_date_time(date, time, tz_offset=0):
    if not date or not time:
        return None

    mytime = datetime.strptime(time, '%H:%M').time()
    mydate = datetime.strptime(date, '%Y-%m-%d')
    mydatetime = datetime.combine(mydate, mytime)

    hours_added = timedelta(hours=-int(tz_offset))
    future_date_and_time = mydatetime + hours_added
    return pytz.utc.localize(future_date_and_time)


def current_yearmonth():
    """
   :Nome da classe/função: current_yearmonth
   :descrição: Função para retornar o anomes atual
   :Criação: Lucas Penha de Moura - 18/04/2022
   :Edições:
   """
    warnings.warn('Deprecated due to new DateTime class .\nUse DateTime.current_period.')
    month = timezone.localtime().month
    year = timezone.localtime().year

    return year * 100 + month


class DateTime:
    def __init__(self):
        self.localtime = timezone.localtime()
        self.monthname_pt = (('jan', 'Janeiro', '01'), ('fev', 'Fevereiro', '02'), ('mar', 'Março', '03'),
                             ('abr', 'Abril', '04'), ('mai', 'Maio', '05'), ('jun', 'Junho', '06'),
                             ('jul', 'Julho', '07'), ('ago', 'Agosto', '08'), ('set', 'Setembro', '09'),
                             ('out', 'Outubro', '10'), ('nov', 'Novembro', '11'), ('dez', 'Dezembro', '12'))

    def current_period(self):
        """
       :Name: current_period
       :Description: Return te current "monthyear" period (mmyyyy)
       :Created by: Lucas Penha de Moura - 18/04/2022
       :Edited by:
       """
        month = timezone.localtime().month
        year = timezone.localtime().year

        return year * 100 + month

    def list_period(self, s_year=2018, s_month=1, e_year=None, e_month=None):
        """
        :Name: list_period
        :Description: Save the information about a category
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        :param s_year: Start year (default 2018)
        :param s_month: Start month (default 1)
        :param e_year: End month
        :param e_month: End month

        Implicit params (passed in the class instance or set by other functions):
        None

        Return: The list of periods between start year/month to end year/mont
        """
        if not e_year and not e_month:
            aux = self.localtime + relativedelta(months=6)
            e_year = aux.year
            e_month = aux.month

        qtd_meses = (e_year - s_year) * 12 + e_month - s_month

        meses = []
        for i in range(0, qtd_meses + 1):
            yearmonth = s_year * 100 + s_month
            aux = {
                'value': yearmonth,
                'text': monthname(s_month) + ' ' + str(s_year),
                'is_now': True if yearmonth == self.current_period() else False,
            }
            meses.append(aux)

            s_month += 1
            if s_month > 12:
                s_month = 1
                s_year += 1

        return meses

    def get_monthname(self, month, starting=1, abbreviated=False):
        """
        :Name: get_monthname
        :Description: Return the name of the month
        :Created by: Lucas Penha de Moura - 18/04/2022

        Explicit params:
        :param month: the number of the month
        :param starting: the index of January (default 1 means January = 1, February = 2, ...)
        :param abbreviated: indicate if the return is full month name or abbreviated

        Implicit params (passed in the class instance or set by other functions):
        None

        Return:
        """

        return self.monthname_pt[month - starting][1] if not abbreviated else self.monthname_pt[month - starting][0]

    @staticmethod
    def get_period(date, is_date_str=False, input_format='%Y-%m-%d'):
        """
        :Name: get_period
        :Description: Get the period from a specific date (yyyymm)
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        :param date: The date to extract the period
        :param is_date_str: indicates if date already in datetime or is string
        :param input_format: the format of date if is_date_str is True

        Implicit params (passed in the class instance or set by other functions):
        None

        Return: The list of periods between start year/month to end year/mont
        """
        if is_date_str:
            date = DateTime.str_to_datetime(date, input_format=input_format)
        referencia_ano = date.year
        referencia_mes = date.month
        return referencia_ano * 100 + referencia_mes

    @staticmethod
    def str_to_datetime(str_date, input_format='%Y-%m-%d'):
        try:
            return datetime.strptime(str_date, input_format)
        except Exception as e:
            print(e)
            return None
