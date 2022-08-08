import warnings
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def format_data(data, mask='____-__-__'):
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
    data_formatada = data

    if data is None or data == '':
        return None

    if mask == '____-__-__':
        cleaned_data = str(data).replace("/", "")

        ano = cleaned_data[4:8]
        mes = cleaned_data[2:4]
        dia = cleaned_data[:2]

        data_formatada = str(ano) + '-' + str(mes) + '-' + str(dia)
    elif mask == '__/__/____':
        cleaned_data = str(data).replace("-", "")

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
    monthname_pt = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
                    "Setembro", "Outubro", "Novembro", "Dezembro")

    return monthname_pt[month - 1]


def split_anomes(anomes=None):
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


def data_to_datetime(anomesdiaformatado, formato='%Y-%m-%d'):
    try:
        return datetime.strptime(anomesdiaformatado, formato)
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
        self.monthname_pt = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

    def current_period(self):
        """
       :Nome da classe/função: current_period
       :descrição: Return te current monthyear period (mmyyyy)
       :Criação: Lucas Penha de Moura - 18/04/2022
       :Edições:
       """
        month = timezone.localtime().month
        year = timezone.localtime().year

        return year * 100 + month

    def list_period(self, s_year=2018, s_month=1, e_year=None, e_month=None):
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

    def get_monthname(self, month, starting=1):
        """
       :Nome da classe/função: get_monthname
       :descrição: Return the name of the month
       :Criação: Lucas Penha de Moura - 18/04/2022
       :param month: the number of the month
       :param starting: The index of Junuary (default 1 means January = 1, February = 2, ...)
       :Edições:
       """

        return self.monthname_pt[month - starting]
