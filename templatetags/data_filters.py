import datetime
from django import template

register = template.Library()

MINUTOS = 60
HORAS = MINUTOS * 60
DIAS = HORAS * 24
SEMANAS = DIAS * 7
MESES = DIAS * 30
ANOS = MESES * 12

@register.filter
def tempo_desde_data(data_desde):
    segundos_atual = datetime.datetime.today().timestamp()
    segundos_desde = data_desde.timestamp()
    diff = int(segundos_atual - segundos_desde)
    anos = int(diff / ANOS)
    meses = int(diff / MESES)
    semanas = int(diff / SEMANAS)
    dias = int(diff / DIAS)
    horas = int(diff / HORAS)
    minutos = int(diff / MINUTOS)

    if anos == 1:
        return '1 ano atrás'
    if anos > 1:
        return str(anos) + ' anos atrás'
    if meses == 1:
        return '1 mes atrás'
    if meses > 1:
        return str(meses) + ' meses atrás'
    if semanas == 1:
        return '1 semana atrás'
    if semanas > 1:
        return str(semanas) + ' semanas atrás'
    if dias == 1:
        return '1 dia atrás'
    if dias > 1:
        return str(dias) + ' dias atrás'
    if horas == 1:
        return '1 hora atrás'
    if horas > 1:
        return str(horas) + ' horas atrás'
    if minutos == 1:
        return '1 minuto atrás'
    if minutos > 1:
        return str(minutos) + ' minutos atrás'
    return str(diff) + ' segundos atrás'
