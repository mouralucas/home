from django.db.models import Case, When, BooleanField, F

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

    def get_category(self, module, id_selected=''):
        categorias = core.models.Category.objects.values('id', 'name', 'description', 'comments').ativos() \
            .annotate(is_selected=Case(When(id=id_selected, then=True),
                                       default=False,
                                       output_field=BooleanField()),
                      id_father=F('father_id'),
                      nm_father=F('father__description')).filter(module=module)

        response = {
            'status': True,
            'categories': list(categorias)
        }

        return response
