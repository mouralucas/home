import os

from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def not_null(value, arg):
    valor_formatado = value

    if arg == 'perc':
        valor_formatado = str(value) + '%'
    elif arg == 'real':
        valor_formatado = 'R$ ' + str(value)
    elif arg == 'dias':
        valor_formatado = str(value) + ' dias'

    return '--' if value is None or value == '' else valor_formatado


@register.filter
def to_underline(value):
    return value.replace('.', '_')


@register.filter
def cor(value):
    colors = {
        1: 'danger',
        2: 'warning',
        3: 'middle',
        4: 'success',
        5: 'info',
    }
    try:
        return colors[value]
    except KeyError:
        return 'secondary'


@register.filter
def trim(value):
    return value.strip()


@register.filter
def file_name(value):
    return str(os.path.basename(value))


@register.filter
def map_name(value):
    depara_nome = {
        'f': 'Filial',
        'r': 'Regional',
        'd': 'Distrital',
    }
    try:
        return depara_nome[value]
    except KeyError:
        return ''


@register.simple_tag
def user_token(value):
    return format_html('<input type="hidden" name="user_token" value="{}">', value)


@register.filter
def nm_estado(value):
    estados = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espirito Santos',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paríba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins',
    }
    try:
        return estados[value.upper()]
    except KeyError:
        return ''
