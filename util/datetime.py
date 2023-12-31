import warnings
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def current_period():
    """
   :Name: current_period
   :Description: Return te current "year/month" period (yyyymm) as integer
   :Created by: Lucas Penha de Moura - 18/04/2022
   :Edited by:
   """
    month = timezone.localtime().month
    year = timezone.localtime().year

    return year * 100 + month


def get_period_from_date(date, is_date_str=False, input_format='%Y-%m-%d'):
    """
    :Name: get_period
    :Description: Get the period from a specific date (yyyymm)
    :Created by: Lucas Penha de Moura - 02/10/2022
    :Edited by:

    :param date: The date to extract the period
    :param is_date_str: indicates if date already in datetime or is string
    :param input_format: the format of date if is_date_str is True

    Return: The list of periods between start year/month to end year/mont
    """
    if is_date_str:
        date = DateTime.str_to_datetime(date, input_format=input_format)
    referencia_ano = date.year
    referencia_mes = date.month
    return referencia_ano * 100 + referencia_mes


def list_period(s_year=None, s_month=None, e_year=None, e_month=None):
    """
    :Name: list_period
    :Description: Save the information about a category
    :Created by: Lucas Penha de Moura - 02/10/2022
    :Edited by:

    Explicit params:
    :param s_year: Start year
    :param s_month: Start month
    :param e_year: End year
    :param e_month: End month

    Return: The list of periods between start year/month to end year/mont
    """
    if not e_year and not e_month:
        aux = timezone.localtime() + relativedelta(months=6)
        e_year = aux.year
        e_month = aux.month

    qtd_meses = (e_year - s_year) * 12 + e_month - s_month

    meses = []
    for i in range(0, qtd_meses + 1):
        yearmonth = s_year * 100 + s_month
        aux = {
            'value': yearmonth,
            'text': get_monthname(s_month) + ' ' + str(s_year),
            'current': True if yearmonth == current_period() else False,
        }
        meses.append(aux)

        s_month += 1
        if s_month > 12:
            s_month = 1
            s_year += 1

    response = {
        'success': True,
        'periods': meses
    }

    return response

def validate_period(value, raise_exception=False):
    """
    :Name: logout
    :Created by: Lucas Penha de Moura - 30/12/2023
    :Edited by:

    Explicit params:
    :param value: the value of period to validation
    :param raise_exception: raise an exception instead of returning False

        Check if the integer value passed contains valid year and month values
    """
    try:
        date_str = str(value)
        datetime.strptime(date_str, '%Y%m')

        return True
    except ValueError as e:
        if raise_exception:
            raise ValueError

        return False


##### OLDER FUNCTIONS REVIEW AND REMOVE UNUSED #####
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


def concat_date_time(date, time, tz_offset=0):
    if not date or not time:
        return None

    mytime = datetime.strptime(time, '%H:%M').time()
    mydate = datetime.strptime(date, '%Y-%m-%d')
    mydatetime = datetime.combine(mydate, mytime)

    hours_added = timedelta(hours=-int(tz_offset))
    future_date_and_time = mydatetime + hours_added
    return pytz.utc.localize(future_date_and_time)


class DateTime:
    # TODO: Utils function show not be in classes, that was an error
    # Review the methods outside the class, remove not used and than remove the class
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
    def str_to_datetime(str_date, input_format='%Y-%m-%d', raise_exception=False):
        try:
            return datetime.strptime(str_date, input_format)
        except Exception as e:
            if raise_exception:
                raise Exception
            return None
