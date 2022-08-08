from django.db.models import Case, When, BooleanField

import core.models
import core.serializers


class Misc:
    def __init__(self):
        pass

    @staticmethod
    def get_language(campos=None, selected_id=None):
        if campos is None:
            campos = ['id', 'name']

        languages = core.models.Language.objects.values(*campos) \
            .annotate(is_selected=Case(When(id=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField())).order_by('name')

        if not languages:
            response = {
                'status': False,
                'descricao': 'Nenhum idioma encontrado'
            }
            return response

        response = {
            'status': True,
            'languages': list(languages)
        }

        return response

    def get_country(self, campos=None):
        if campos is None:
            campos = ['codigo', 'nome']

        contries = core.models.Pais.objects.order_by('codigo')

        if not contries:
            response = {
                'status': False,
                'descricao': 'Nenhum idioma encontrado'
            }
            return response

        response = {
            'status': True,
            'countries': core.serializers.PaisSerializer(contries, many=True, fields=campos).data
        }

        return response

    def get_currency(self):
        currency = [{'value': i[0], 'text': i[1]} for i in core.models.CyrruncyTypes.choices]

        response = {
            'status': True,
            'qtd': len(currency),
            'currency': currency
        }

        return response
